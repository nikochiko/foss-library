# FOSS Library

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

## Screenshots

<img width="1440" alt="Screenshot 2021-09-10 at 5 07 06 PM" src="https://user-images.githubusercontent.com/37668193/132847979-c78fce59-823c-4990-afd4-8e95e3266b2b.png">

<hr />

<img width="1440" alt="Screenshot 2021-09-10 at 5 07 09 PM" src="https://user-images.githubusercontent.com/37668193/132847987-ffee6cd3-19b5-4a25-ba30-4d8a3c5b7975.png">

<hr />

<img width="1440" alt="Screenshot 2021-09-10 at 5 07 15 PM" src="https://user-images.githubusercontent.com/37668193/132848012-a374a5a1-086f-41a0-b6fc-9ce30ec09435.png">

<hr />

<img width="1440" alt="Screenshot 2021-09-10 at 5 07 26 PM" src="https://user-images.githubusercontent.com/37668193/132848026-852b77cd-0c8b-4f53-912d-657375a53a23.png">

<hr />

<img width="1440" alt="Screenshot 2021-09-10 at 5 07 35 PM" src="https://user-images.githubusercontent.com/37668193/132848033-cbef8c26-93f2-4ad4-816e-2859ec02874b.png">

<hr />

<img width="1440" alt="Screenshot 2021-09-10 at 5 07 56 PM" src="https://user-images.githubusercontent.com/37668193/132848042-1531ed47-6c0f-478b-9caa-b848ad6f6a5c.png">

<hr />

<img width="1440" alt="Screenshot 2021-09-10 at 5 08 04 PM" src="https://user-images.githubusercontent.com/37668193/132848053-8cfcc211-3fbd-4709-aa89-4d7f50e5cf3e.png">
