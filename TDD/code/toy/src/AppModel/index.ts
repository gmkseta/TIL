import { PositiveIntegerGenerator } from './PositiveIntegerGenerator';

const NEW_LINE = '\n';


interface Processor {
  call: (self: AppModel, input: string) => Processor;
}
// run -> call

export class AppModel {
  private completed = false
  private readonly SELECT_MODE_MESSAGE = `1: Single player game${NEW_LINE}2: Multiplayer game${NEW_LINE}3: Exit${NEW_LINE}Enter selection: `;

  private output = this.SELECT_MODE_MESSAGE
  private generator: PositiveIntegerGenerator;
  private processor: Processor;


  public constructor(generator: PositiveIntegerGenerator) {
    this.generator = generator;
    this.processor = this.preocessModelSelection;
  }

  public isCompleted = (): boolean => {
    return this.completed;
  }

  public flushOutput = (): string | null =>{
    return this.output;
  }

  public processInput(input: string) {
    this.processor = this.processor.call(this, input);
  }

  private preocessModelSelection(input: string): Processor {
    if (input === "1") {
      this.output = "Single player game" + NEW_LINE + "I'm thinking of a number between 1 and 100."
        + NEW_LINE + "Enter your guess: ";
      const answer = this.generator.generateLessThanOrEqualToHundread();
      return this.getSinglePlayerProcessor(answer, 1);
    }else{
      this.completed = true;
      return this.preocessModelSelection
      
    }
    // ?? 
  }


  private getSinglePlayerProcessor(answer: number, tries: number): Processor {
    return (input: string) => {
        let guess = parseInt(input);
        if (guess < answer) {
          this.output = "Your guess is too low." + NEW_LINE + "Enter your guess: ";
          return this.getSinglePlayerProcessor(answer, tries + 1);
        } else if (guess > answer) {
          this.output = "Your guess is too high." + NEW_LINE + "Enter your guess: ";
          return this.getSinglePlayerProcessor(answer, tries + 1);
        } else {
          this.output = "Correct! " + tries + (tries == 1 ? " guess." : " guesses.") + NEW_LINE + this.SELECT_MODE_MESSAGE
          return this.preocessModelSelection
        }
      }
    }
}
