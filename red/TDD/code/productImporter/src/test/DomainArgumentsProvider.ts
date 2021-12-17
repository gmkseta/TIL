import { DomainArgumentResolver } from "./DomainArgumentResolver";
import { DomainArgumentsSource } from "./DomainArgumentsSource";

//implements ArgumentsProvider, AnnotationConsumer<DomainArgumentsSource> 
export class DomainArgumentsProvider {

    public accept(annotation: DomainArgumentsSource):void {
    }

    public provideArguments(context) {
        Method method = context.getRequiredTestMethod();
        Class<?>[] parameterTypes = method.getParameterTypes();

        const arguments = new Object[parameterTypes.length];
        const argumentResolver: DomainArgumentResolver = DomainArgumentResolver.instance;
        for (int i = 0; i < arguments.length; i++) {
            Optional<Object> argument = argumentResolver.tryResolve(parameterTypes[i]);
            arguments[i] = argument.orElse(null);
        }

        return Arrays.stream(new Arguments[] { Arguments.of(arguments) });
    }

}
