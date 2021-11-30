import { Product } from "./Product";


export interface ProductValidator {
  isValid: (product: Product) => boolean;
}
