## Elasticsearch 中 FST 的实现原理

​		在3月初的时候，接到一个重构 ES 部分数据的需求，于是我开始学习了解这个 **分布式全文搜索引擎**，其中对 Lucene 中 term index 使用的数据结构 FST 比较感兴趣，在学习原理后，使用 Python 实现了一个简易版的 FST 。

#### 第一节  简单介绍 Elasticsearch

> 	Elasticsearch 是一个开源的搜索引擎，建立在一个全文搜索引擎库 [Apache Lucene™](https://lucene.apache.org/core/) 基础之上。 Lucene 可以说是当下最先进、高性能、全功能的搜索引擎库—无论是开源还是私有。 
> 	
> 但是 Lucene 仅仅只是一个库，且 Lucene *非常* 复杂。
> 	
> Elasticsearch 内部使用 Lucene 做索引与搜索，通过隐藏 Lucene 的复杂性，取而代之的提供一套简单一致的 RESTful API。
> 	
> 然而，Elasticsearch 不仅仅是 Lucene，并且也不仅仅只是一个全文搜索引擎。 它可以被下面这样准确的形容：
>
> - 一个*分布式* 的实时文档存储，*每个字段* 可以被索引与搜索
> - 一个*分布式* 实时分析搜索引擎
> - 能胜任上百个服务节点的扩展，并支持 PB 级别的结构化或者非结构化数据
Elasticsearch 将所有的功能打包成一个单独的服务，这样你可以通过程序与它提供的简单的 RESTful API 进行通信， 可以使用自己喜欢的编程语言充当 web 客户端。

​		

下面介绍一些基本概念，文档，索引，分片，字段

  ```json
// 插入一个文档，索引名为 test, 类型为 _doc, 唯一ID为1
// 以 Mysql 的视角而言: 索引是一张表，文档是一条数据，ID 则为主键

POST test/_doc/1       // [method] index/type/_id
{
  "book_id": "1",
  "title": "挪威的深林",
  "author": "村上春树",
  "price": 33.5,
  "public": "1998-03-11"
}

// 新数据插入以后，es 会自动添加一些元数据，以 _ 开头
// 获取ID为 1 的数据
GET test/_doc/1
{
  "_index" : "test",		//	文档所属的索引名
  "_type" : "_doc",			//	文档所属的类型名
  "_id" : "1",				//	文档的唯一ID
  "_version" : 1,			//	文档的版本信息
  "_source" : {				//	文档的原始 json 内容 
    "book_id" : "1",
    "title" : "挪威深林",
    "arthor" : "村上春树",
    "price" : 33.5,
    "public" : "1998-03-11"
  }
}

// mapping 类似 mysql 中的列，第一次插入数据会自动推断生成，也可以手动定义 mapping 。

GET test/_mapping		// 如果没有在创建Index 指定 mapping, es 会通过类型推测创建 mapping
{
  "test" : {
    "mappings" : {
      "properties" : {
        "author" : {
          "type" : "text",	 // 一般 string 类型的字段会被动态设别为 text 类型，text 类型会分词
          "fields" : {		 // es 支持一个字段多个子类型	
            "keyword" : {		// 子类型名为 keyword 查询的时候可以使用 {author.keyword: xxx}
              "type" : "keyword",	// keyword 类型就是 string 类型，但是不会进行分词
              "ignore_above" : 256	// 默认生成的 keyword 子字段只保留主字段内容的前 256 个字符
            }
          }
        },
        "book_id" : {},  		// 同author 
        "title": {},			// 同 author
        "price" : {
          "type" : "float"		// 33.5 自动推断为 浮点 类型
        },
        "public" : {
          "type" : "date"		// "1998-03-11" 自动推断为 日期 类型
        },
        }
      }
    }
  }
}

  ```



#### 第二节  elasticsearch 索引内部原理

###### 1. 数据是如何被搜索到的

​		 在传统数据库中，每个字段都只存储单个值，搜索都是建立在某个字段某个值上（尽管有模糊搜索之类的东西，但是也是拿出某个值来匹配）。 而全文检索要求的是，每个单词都能被索引，也就是一个字段可以索引多个值。例如  ｛"text": "aaa  bbb  ccc"｝，使用 aaa 或 bbb 或ccc 都能索引到 text 这个字段。

> 对 一个字段多个值 支持的数据结构就是 **倒排索引** 了
>
> 倒排索引包含一个有序列表，列表包含所有文档出现过的不重复个体，或称为 term，对于每一个 term，包含了它所有曾出现过文档的列表。
>
> ```
> Term  | Doc 1 | Doc 2 | Doc 3 | ...
> ------------------------------------
> brown |   ✔   |       |  ✔    | ...
> fox   |   ✔   |   ✔   |  ✔    | ...
> quick |   ✔   |   ✔   |       | ...
> the   |   ✔   |       |  ✔    | ...
> ```
> 当讨论倒排索引时，大家会认为只有在 text 这种分词的长字符串字段才使用倒排索引，事实上，在文档中， 每个被索引的字段都有自己的倒排索引。



**索引是不可变的** 

​		后面讲 FST 会解释这个不可变的原因，下面从官方文档看看它的优缺点。

> 不变性优点如下：
>
> - 不需要锁。如果你从来不更新索引，你就不需要担心多进程同时修改数据的问题。
>
> - 一旦索引被读入内核的文件系统缓存，便会留在哪里，由于其不变性。只要文件系统缓存中还有足够的空间，那么大部分读请求会直接请求内存，而不会命中磁盘。这提供了很大的性能提升。
>
> - 其它缓存(像filter缓存)，在索引的生命周期内始终有效。它们不需要在每次数据改变时被重建，因为数据不会变化。
>
> - 写入单个大的倒排索引允许数据被压缩，减少磁盘 I/O 和 需要被缓存到内存的索引的使用量。
>
> 缺点:
>
> - 因为不可变性，不能修改，如果想要让一个新的文档 可被搜索，你需要重建整个索引。
>
> -  无法直接执行删除操作，只能通过一个 .del 文件标记删除，在合并索引的时候才能真正删除
> - 更新操作转换为 删除 -> 创建 。

​		解决上面确定最简单的方法，就是建立更多的索引，通过增加新的补充索引来反映新近的修改，而不是直接重写整个倒排索引。每一个倒排索引都会被轮流查询到—从最早的开始—查询完后再对结果进行合并。



**搜索是近实时的**

​		在 Lucence 中，一个 index（索引） 包含了多个可以被搜索的 segment （段），上面说的倒排索引，就是一个个的 segment 。

​		ES 中提供了一个 refresh  API 。

> 在 Elasticsearch 中，写入和打开一个 segment 的轻量的过程叫做 *refresh* 。 默认情况下每个分片会每 1s 自动刷新一次。这就是为什么我们说 Elasticsearch 是 *近* 实时搜索: 文档的变化并不是立即对搜索可见，但会在一秒之内变为可见。
>
> 这些行为可能会对新用户造成困惑: 他们索引了一个文档然后尝试搜索它，但却没有搜到。这个问题的解决办法是用 `refresh` API 执行一次手动刷新:

​		在每次 refresh 的时候，会写入一个新 segment ，创建新的 segment 和提供搜索虽然很快，但是过多的 segment 会占用很多系统资源，导致 cpu ，文件句柄不足。



**segment 合并**

> 由于自动 refresh 每秒会创建一个新的段 ，这样会导致短时间内的段数量暴增。而段数目太多会带来较大的麻烦。 每一个段都会消耗文件句柄、内存和cpu运行周期。更重要的是，每个搜索请求都必须轮流检查每个段；所以段越多，搜索也就越慢。
>
> Elasticsearch通过在后台进行段合并来解决这个问题。小的段被合并到大的段，然后这些大的段再被合并到更大的段。





#### 第三节  Lucene 是如何搜索数据的

​		前文说到了倒排索引，让我们用几条数据来模拟一下倒排索引的存储情况。


| Doc_Id | Name | Age  | Sex    |
| ------ | ---- | ---- | ------ |
| 1      | Kate | 24   | Female |
| 2      | John | 24   | Male   |
| 3      | Bill | 29   | Male   |

​		当插入这 3 条数据以后，除去 Doc_Id 有3个常规字段，lucene 会创建 3 个倒排索引，如下：

**Name** 字段的倒排索引：

| Term | Posting List |
| ---- | ------------ |
| Kate | 1            |
| Join | 2            |
| Bill | 3            |

**Age** 字段的倒排索引：

| Term | Posting List |
| ---- | ------------ |
| 24   | 1, 2         |
| 29   | 2            |

**Sex** 字段的倒排索引：

| Term   | Posting List |
| ------ | ------------ |
| Female | 1            |
| Male   | 3            |

​		可见为每个 field 都建立了一个倒排索引。其中 **Posting list** 就是一个 int 的数组，存储了所有符合某个term的文档 doc_id。

​		当我们的 term 很多的时候，比如：

> Carla, Sara, Elin, Ada, Patty, Kate, Selena

​		如果按照这样的顺序排列，找出某个特定的 term 一定很慢，因为 term 没有排序，需要全部过滤一遍才能找出特定的 term。排序之后就变成了：

> Ada,Carla,Elin,Kate,Patty,Sara,Selena

​		这样我们可以用二分查找的方式，比全遍历更快地找出目标的 term。这个就是 term dictionary。有了 term dictionary 之后，可以用 logN 次磁盘查找得到目标。

​		但是磁盘的随机读操作仍然是非常昂贵的（一次 random access 大概需要 10ms 的时间）。所以尽量少的读磁盘，有必要把一些数据缓存到 内存里。但是整个 term dictionary 本身又太大了，无法完整地放到内存里。于是就有了 term index。它相当于一个字典，输入 term，得到 term dictionary 的位置，再获取倒排数组 。从

​		从 lucene4开始，为了方便实现前缀，后缀等复杂的查询语句，lucene使用 FST 数据结构来实现 term index。由于使用 FST 实现的 term index 非常小，可以常驻在内存中，这让搜索变得非常快。
![img](https://pic3.zhimg.com/80/v2-926c47383573f70da40475d2ae2777ce_720w.jpg)		上面这张图就表示 lucene 索引的过程，先从 term index 中获取 term dict 磁盘中的地址，然后取出 term dict地址内容中的 Posting list (倒排索引)。

​		最后，lucene 为了高效搜索使用非常多的数据结构和算法，包括不限于下：

- Term index:  **FST (Finite State Transducers 有限状态传感器)**

- 倒排索引列表合并： **skip list(跳表)**， **bitset(位数组)**
- 范围搜索：**BKDTree (一种支持多维数据的搜索树，很复杂)**
- 排序：**DocValues(列式存储)**



#### 第四节  什么是 FST（Finite State Transducers 有限状态传感器）

​		要了解 FST ，我们要从它最简单的形态，FSM（finite state machine 有限状态机）说起

​			

