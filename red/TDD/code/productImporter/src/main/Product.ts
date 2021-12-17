import { Pricing } from "./Pricing";

export class Product {
    private supplierName: string;
    private productCode: string;
    private productName: string;
    private pricing: Pricing;

    constructor(supplierName :string,  productCode :string,  productName :string, pricing: Pricing) {
        this.supplierName = supplierName;
        this.productCode = productCode;
        this.productName = productName;
        this.pricing = pricing;
    }

    public getSupplierName(): string {
        return this.supplierName;
    }

    public getProductCode(): string {
        return this.productCode;
    }

    public getProductName(): string {
        return this.productName;
    }

    public getPricing(): Pricing {
        return this.pricing;
    }
}
