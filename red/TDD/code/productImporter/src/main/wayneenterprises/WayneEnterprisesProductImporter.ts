import { Product } from "../Product";
import { ProductImporter } from "../ProductImporter";
import { WayneEnterprisesProductSource } from "./WayneEnterprisesProductSource";
import { WayneEnterprisesProductTranslator } from "./WayneEnterprisesProductTranslator";

export class WayneEnterprisesProductImporter implements ProductImporter {

    private dataSource: WayneEnterprisesProductSource;
    private translator: WayneEnterprisesProductTranslator;

    public constructor(dataSource: WayneEnterprisesProductSource) {
        this.dataSource = dataSource;
        this.translator = new WayneEnterprisesProductTranslator();
    }

    public fetchProducts(): Iterable<Product>  {
        return Array.from(this.dataSource.fetchProducts()).map(this.translator.translateProduct);
    }

}
