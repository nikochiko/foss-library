# Frappe Library

CRUD app for managing Books and Members.

## How it is structured?

* Books are the individual books in the library, each one has a separate ID. But there could be multiple
books with the same ISBN.

Schema for books table:

```sql
Book {
  id                    bigint          primary key
  isbn                  string          index
  isbn13                string          index
  title                 string
  authors               string
  average_rating        double precision
  language_code         string
  num_pages             bigint
  ratings_count         bigint
  text_reviews_count    bigint
  publication_date      timestamp
  publisher_name        string

  other indexes:
    lower(authors) using btree text_pattern_ops
    lower(publisher_name) using btree text_pattern_ops
    lower(title) using btree text_pattern_ops
}
```

* Member

```sql
Member {
  id    bigint  primary key
  name  string
}
```

* Transaction

```
Transaction {
  id            bigint          primary key
  book_id       bigint          foreign key (Books)
  member_id     bigint          foreign key (Members)
  borrowed_at   timestamp
  returned_at   timestamp
}
```
