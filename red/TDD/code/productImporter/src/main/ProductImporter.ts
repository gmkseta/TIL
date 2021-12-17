import { Product } from "./Product";

export interface ProductImporter {
    fetchProducts: () => Iterable<Product> ;
}
