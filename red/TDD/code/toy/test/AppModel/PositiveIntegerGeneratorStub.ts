import { PositiveIntegerGenerator } from "../../src/AppModel/PositiveIntegerGenerator";

export class PositiveIntegerGeneratorStub implements PositiveIntegerGenerator {
  private readonly numbers: number[];
  private index: number;
  constructor(...numbers: number[]) {
    this.numbers = numbers;
    this.index = 0;
  }

  generateLessThanOrEqualToHundread(): number {
    let num = this.numbers[this.index];
    this.index = (this.index + 1) % this.numbers.length;
    return num;
  }
  
}