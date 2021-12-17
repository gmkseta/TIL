import { Product } from "./Product";
import { ProductValidator } from "./ProductValidator";

export class ListPriceFilter implements ProductValidator {

    private lowerBound: number;

    public constructor(lowerBound: number) {
        this.lowerBound = lowerBound;
    }

    public isValid(product: Product): boolean {
        return product.getPricing().getListPrice() >= this.lowerBound;
    }

}
