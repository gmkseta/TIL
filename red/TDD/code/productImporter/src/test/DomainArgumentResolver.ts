import { CompositeArgumentResolver } from "./CompositeArgumentResolver";
import { WayneEnterprisesProductArgumentResolver } from "./suppliers/wayneenterprises/WayneEnterprisesProductArgumentResolver";

export abstract class DomainArgumentResolver {
    private random: number = Math.random();
    public static instance: DomainArgumentResolver;

    public abstract tryResolve(product: any): any;

    public constructor(){
        DomainArgumentResolver.instance = new CompositeArgumentResolver(new WayneEnterprisesProductArgumentResolver());
    }
}
