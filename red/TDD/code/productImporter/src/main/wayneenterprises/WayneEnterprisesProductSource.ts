import { WayneEnterprisesProduct } from "./WayneEnterprisesProduct";

export interface WayneEnterprisesProductSource {
    fetchProducts: () => Iterable<WayneEnterprisesProduct> ;
}
