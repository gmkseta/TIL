import { PositiveIntegerGenerator } from "./AppModel/PositiveIntegerGenerator";



export class RandomGenerator implements PositiveIntegerGenerator {
    private readonly random = Math.random;

    public generateLessThanOrEqualToHundread = (): number=> {
        return parseInt(`${this.random()*100}`)
    }
}
