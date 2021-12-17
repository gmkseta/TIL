export class Pricing {
    private listPrice: number;
    private discount: number;

    constructor(listPrice: number, discount: number) {
        this.listPrice = listPrice;
        this.discount = discount;
    }

    public getListPrice(): number {
        return this.listPrice;
    }

    public getDiscount(): number {
        return this.discount;
    }
}
