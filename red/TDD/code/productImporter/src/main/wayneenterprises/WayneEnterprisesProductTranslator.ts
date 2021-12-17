import { Pricing } from "../Pricing";
import { Product } from "../Product";
import { WayneEnterprisesProduct } from "./WayneEnterprisesProduct";

export class WayneEnterprisesProductTranslator {
    public translateProduct(source: WayneEnterprisesProduct): Product {
        const pricing: Pricing = this.getPricing(source);
        return new Product("WAYNE", source.getId(), source.getTitle(), pricing);
    }

    private getPricing(source: WayneEnterprisesProduct): Pricing {
        const listPrice: number = source.getListPrice()
        const discount: number = source.getListPrice() - source.getSellingPrice()
        return new Pricing(listPrice, discount);
    }
}
