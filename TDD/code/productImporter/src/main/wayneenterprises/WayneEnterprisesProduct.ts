
export class WayneEnterprisesProduct {
    private id: string;
    private title: string;
    private listPrice: number;
    private sellingPrice: number;

    public constructor(id: string, title: string, listPrice: number, sellingPrice: number) {
        this.id = id;
        this.title = title;
        this.listPrice = listPrice;
        this.sellingPrice = sellingPrice;
    }

    public getId(): string {
        return this.id;
    }

    public getTitle(): string {
        return this.title;
    }

    public getListPrice(): number {
        return this.listPrice;
    }

    public getSellingPrice(): number {
        return this.sellingPrice;
    }
}
