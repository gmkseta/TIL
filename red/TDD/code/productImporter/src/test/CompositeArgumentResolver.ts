import { DomainArgumentResolver } from "./DomainArgumentResolver";

export class CompositeArgumentResolver extends DomainArgumentResolver {

    private resolvers: DomainArgumentResolver[] ;

    public constructor(...resolvers: DomainArgumentResolver[]) {
        super()
        this.resolvers = resolvers;
    }

    public tryResolve(parameterType: any) {
        for (const resolver of this.resolvers) {
            const argument = resolver.tryResolve(parameterType);
            if (argument.isPresent()) {
                return argument;
            }
        }

        return null;
    }

}
