import { Product } from "./Product";

export interface ProductInventory {
    upsertProduct: (product: Product) => void;
}
