import { ProductImporter } from "./ProductImporter";
import { ProductInventory } from "./ProductInventory";
import { ProductValidator } from "./ProductValidator";

export class ProductSynchronizer {
    private importer: ProductImporter;
    private validator: ProductValidator;
    private inventory: ProductInventory;

    public constructor(importer: ProductImporter, validator: ProductValidator, inventory: ProductInventory) {
        this.importer = importer;
        this.validator = validator;
        this.inventory = inventory;
    }

    public run(): void {
        for (const product of this.importer.fetchProducts()) {
            if (this.validator.isValid(product)) {
                this.inventory.upsertProduct(product);
            }
        }
    }
}
