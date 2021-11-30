import { WayneEnterprisesProduct } from '../../../main/wayneenterprises/WayneEnterprisesProduct';
import { WayneEnterprisesProductSource } from '../../../main/wayneenterprises/WayneEnterprisesProductSource';

export class WayneEnterprisesProductSourceStub implements WayneEnterprisesProductSource {

    private products:  WayneEnterprisesProduct[];

    public constructor(products: WayneEnterprisesProduct[]) {
        this.products = products;
    }

    public fetchProducts(): Iterable<WayneEnterprisesProduct>  {
        return Array.from(this.products);
    }

}
