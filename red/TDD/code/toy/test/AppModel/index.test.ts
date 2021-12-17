import { AppModel } from '../../src/AppModel';
import { PositiveIntegerGeneratorStub } from './PositiveIntegerGeneratorStub';

const NEW_LINE = '\n';

describe('AppModel ', () => {
  test('should be incompleted', () => {
    const appModel = new AppModel(new PositiveIntegerGeneratorStub(50));
    const actual = appModel.isCompleted();
    expect(actual).toBe(false);
  });

  test('correctly prints select mode message', () => {
    const appModel = new AppModel(new PositiveIntegerGeneratorStub(50));
    const actual = appModel.flushOutput();
    expect(actual).toBe(`1: Single player game${NEW_LINE}2: Multiplayer game${NEW_LINE}3: Exit${NEW_LINE}Enter selection: `);
  });

  test('correctly exists', () => {
    const appModel = new AppModel(new PositiveIntegerGeneratorStub(50));

    appModel.processInput('3');

    const actual = appModel.isCompleted();

    expect(actual).toBe(true);
  });

  test('sut_correctly_prints_single_player_game_start_message', () => {
    const sut = new AppModel(new PositiveIntegerGeneratorStub(50));
    sut.flushOutput();
    sut.processInput('1');

    const actual = sut.flushOutput();
    expect(actual).toBe(`Single player game${NEW_LINE}I'm thinking of a number between 1 and 100.${
      NEW_LINE}Enter your guess: `);
  });
});

describe('AppModel Answer and Guess', () => {
  test.each`
    answer | guess
    ${50} | ${40}
    ${30} | ${29}
    ${89} | ${9}
  `(
    'sut_correctly_prints_too_low_message_in_single_player_game using $answer, $guess',
    ({ answer, guess }) => {
      const sut = new AppModel(new PositiveIntegerGeneratorStub(answer));
      sut.processInput('1');
      sut.flushOutput();
      sut.processInput(guess.toString());
      const actual = sut.flushOutput();

      expect(actual).toBe(`Your guess is too low.${NEW_LINE}Enter your guess: `);
    },
  );

  test.each`
      answer | guess
      ${50} | ${60}
      ${80} | ${81}
    `('sut_correctly_prints_too_high_message_in_single_player_game using $answer, $guess', ({ answer, guess }) => {
    const sut = new AppModel(new PositiveIntegerGeneratorStub(answer));
    sut.processInput('1');
    sut.flushOutput();
    sut.processInput(guess.toString());
    const actual = sut.flushOutput();
    expect(actual).toBe(`Your guess is too high.${NEW_LINE}Enter your guess: `);
  });

  test.each`
      answer 
      ${1}
      ${10}
      ${100}
    `('sut_correctly_prints_correct_answer_message_in_single_player_game using $answer', ({ answer }) => {
    const sut = new AppModel(new PositiveIntegerGeneratorStub(answer));
    sut.processInput('1');
    sut.flushOutput();
    const guess = answer;
    sut.processInput(guess.toString());
    const actual = sut.flushOutput();
    expect(actual).toMatch(new RegExp('^Correct\!'));
  });

  test.each`
      fails 
      ${1}
      ${10}
      ${100}
    `('sut correctly prints guess count if single player game finished using $fails', ({ fails }) => {
    const sut = new AppModel(new PositiveIntegerGeneratorStub(50));
    sut.processInput('1');
    for (let i = 0; i < fails; i++) {
      sut.processInput('30');
    }
    sut.flushOutput();
    sut.processInput('50');
    const actual = sut.flushOutput();
    expect(actual).toMatch(new RegExp(`.*${(fails + 1)} guesses\..*`));
  });

  test('sut correctly prints one guess if single player game finished', () => {
    const sut = new AppModel(new PositiveIntegerGeneratorStub(50));
    sut.processInput('1');
    sut.flushOutput();
    sut.processInput('50');
    const actual = sut.flushOutput();
    expect(actual).toMatch(new RegExp('.*1 guess\..*'));
  });

  // sut prints select mode message if single player game finished
  test('sut prints select mode message if single player game finished', () => {
    const sut = new AppModel(new PositiveIntegerGeneratorStub(50));
    sut.processInput('1');
    sut.flushOutput();
    sut.processInput('50');
    const actual = sut.flushOutput();
    expect(actual).toMatch(new RegExp(
      `.*1: Single player game${NEW_LINE}2: Multiplayer game${NEW_LINE}3: Exit${NEW_LINE}Enter selection: `,
    ));
  });

  // sut returns to mode selection if single player game finished
  test('sut returns to mode selection if single player game finished', () => {
    const sut = new AppModel(new PositiveIntegerGeneratorStub(50));
    sut.processInput('1');
    sut.processInput('50');
    sut.processInput('3');
    const actual = sut.isCompleted();
    expect(actual).toBe(true);
  });

  // sut generates answer for each game
  test.each`
    source 
    ${'1,10,100'}
  `('sut generates answer for each game $source', ({ source }) => {
    const answers: number[] = source.split(',').map((v: string) => parseInt(v));
    const sut = new AppModel(new PositiveIntegerGeneratorStub(...answers));

    for (const answer of answers) {
      sut.processInput('1');
      sut.flushOutput();
      sut.processInput(answer.toString());
    }

    const actual = sut.flushOutput();
    expect(actual).toMatch(new RegExp('^Correct\!'));
  });
});

describe("For Multiplay", ()=>{
  test('sut_correctly_prints_too_low_message_in_multiplayer_game', ()=>{
    const sut = new AppModel(new PositiveIntegerGeneratorStub(50));
    sut.flushOutput();
    sut.processInput('2');
    const actual = sut.flushOutput();
    expect(actual).toBe("Multiplayer game" + NEW_LINE + "Enter player names separated with commas: ");
  })

  test('sut_correctly_prints_multiplayer_game_start_message', ()=>{
    const sut = new AppModel(new PositiveIntegerGeneratorStub(50));
    sut.processInput('2');
    sut.flushOutput();
    sut.processInput('player1,player2');
    const actual = sut.flushOutput();

    expect(actual).toMatch(new RegExp(`^player1, player2${NEW_LINE}I'm thinking of a number between 1 and 100.`));
  })

  //sut correctly prompts first player name in multiplayer game
  test.each`
    player1 | player2 | player3
    ${'player1'} | ${'player2'} | ${'player3'}
    ${'player2'} | ${'player3'} | ${'player1'}
    ${'player3'} | ${'player1'} | ${'player2'}
  `('sut correctly prompts first player name in multiplayer game $player1, $player2, $player3', ({ player1, player2, player3 }) => {
    const sut = new AppModel(new PositiveIntegerGeneratorStub(50));
    sut.processInput('2');
    sut.flushOutput();
    sut.processInput(`${player1},${player2},${player3}`);
    const actual = sut.flushOutput();

    expect(actual).toMatch(new RegExp(`.*${player1}'s turn. Enter your guess: `));
  })

  //sut correctly prompts second player name in multiplayer game
  test.each`
    player1 | player2 | player3
    ${'player1'} | ${'player2'} | ${'player3'}
    ${'player2'} | ${'player3'} | ${'player1'}
    ${'player3'} | ${'player1'} | ${'player2'}
  `('sut correctly prompts second player name in multiplayer game $player1, $player2, $player3', ({ player1, player2, player3 }) => {
    const sut = new AppModel(new PositiveIntegerGeneratorStub(50));
    sut.processInput('2');
    sut.processInput(`${player1},${player2},${player3}`);
    sut.flushOutput();
    sut.processInput('10');
    const actual = sut.flushOutput();

    expect(actual).toMatch(new RegExp(`.*${player2}'s turn. Enter your guess: `));
  })

  //sut correctly prompts third player name in multiplayer game
  test.each`
    player1 | player2 | player3
    ${'player1'} | ${'player2'} | ${'player3'}
    ${'player2'} | ${'player3'} | ${'player1'}
    ${'player3'} | ${'player1'} | ${'player2'}
  `('sut correctly prompts third player name in multiplayer game $player1, $player2, $player3', ({ player1, player2, player3 }) => {
    const sut = new AppModel(new PositiveIntegerGeneratorStub(50));
    sut.processInput('2');
    sut.processInput(`${player1},${player2},${player3}`);
    sut.flushOutput();
    sut.processInput('20');
    const actual = sut.flushOutput();

    expect(actual).toMatch(new RegExp(`.*${player3}'s turn. Enter your guess: `));
  })


}) 

