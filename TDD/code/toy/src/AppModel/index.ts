import { PositiveIntegerGenerator } from './PositiveIntegerGenerator';

const NEW_LINE = '\n';

export class AppModel {
  private completed = false
  private readonly SELECT_MODE_MESSAGE = `1: Single player game${NEW_LINE}2: Multiplayer game${NEW_LINE}3: Exit${NEW_LINE}Enter selection: `;

  private output = this.SELECT_MODE_MESSAGE
  private answer!: number;
  private singlePlayerMode: boolean;
  private tries: number;
  private generator: PositiveIntegerGenerator;

  public constructor(generator: PositiveIntegerGenerator) {
    this.generator = generator;
    this.singlePlayerMode = false
    this.tries = 0;
  }

  public isCompleted = (): boolean => {
    return this.completed;
  }

  public flushOutput = (): string | null =>{
    return this.output;
  }

  public processInput(input: string) {
    if(this.singlePlayerMode){
      this.processSinglePlayerGame(input);
    }else{
      this.preocessSelection(input);
    }
  }

  private processSinglePlayerGame(input: string) {
    let guess = parseInt(input);
    this.tries++
    if (guess < this.answer) {
      this.output = "Your guess is too low." + NEW_LINE + "Enter your guess: ";
    } else if (guess > this.answer) {
      this.output = "Your guess is too high." + NEW_LINE + "Enter your guess: ";
    } else {
      this.output = "Correct! " + this.tries + (this.tries == 1 ? " guess." : " guesses.") + NEW_LINE + this.SELECT_MODE_MESSAGE
      this.singlePlayerMode = false;
      
    }
  }

  private preocessSelection(input: string) {
    if (input === "1") {
      this.output = "Single player game" + NEW_LINE + "I'm thinking of a number between 1 and 100."
        + NEW_LINE + "Enter your guess: ";
      this.singlePlayerMode = true;
      this.answer = this.generator.generateLessThanOrEqualToHundread();
    }else{
      this.completed = true;
    }
  }
}

