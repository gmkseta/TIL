import { WayneEnterprisesProduct } from "../../../main/wayneenterprises/WayneEnterprisesProduct";
import { DomainArgumentResolver } from "../../DomainArgumentResolver";


function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
    })
}

export class WayneEnterprisesProductArgumentResolver extends DomainArgumentResolver {

    public tryResolve(parameterType: WayneEnterprisesProduct | WayneEnterprisesProduct[]): any {
        const generate = WayneEnterprisesProductArgumentResolver.generate
        if (parameterType instanceof WayneEnterprisesProduct) {
            return generate();
        } else if (parameterType instanceof Array) {
            return [generate(), generate(), generate()];
        }

        return null;
    }

    private static generate(): WayneEnterprisesProduct {
        const id: string = "id" + uuidv4();
        const title: string = "title" + uuidv4();
        const listPrice: number = parseInt(`${Math.random()*100000 + 100000}`);
        const sellingPrice: number = listPrice - parseInt(`${Math.random()*10000 + 10000}`);
        return new WayneEnterprisesProduct(id, title, listPrice, sellingPrice);
    }

}