import "@typespec/http";

using TypeSpec.Http;

@service({
  title: "Library Management API",
  version: "1.0.0",
})
@server("http://api.library.local/v1", "Local Server")
namespace LibraryApi;

model Book {
  @example(101)
  id: int32;

  @example("The Lord of the Rings")
  title: string;

  @example("J.R.R. Tolkien")
  author: string;

  @example(1954)
  publishedYear?: int32;
}

model BookInput {
  @example("The Lord of the Rings")
  title: string;

  @example("J.R.R. Tolkien")
  author: string;

  @example(1954)
  publishedYear?: int32;
}

model Error {
  error: string;
}

@route("/books")
interface Books {
  @summary("Get all books")
  @get
  list(): Book[];

  @summary("Add a new book")
  @post
  create(@body book: BookInput): {
    @statusCode code: 201;
    @body book: Book;
  } | {
    @statusCode code: 400;
    @body error: Error;
  };

  @summary("Get a book by ID")
  @route("/{id}")
  @get
  read(@path id: int32): Book | {
    @statusCode code: 404;
    @body error: Error;
  };
}
