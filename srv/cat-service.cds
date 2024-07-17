using my.bookshop as my from '../db/data-model';

@(requires: 'authenticated-user')
service CatalogService {
    @readonly
    entity Books as projection on my.Books;
}
