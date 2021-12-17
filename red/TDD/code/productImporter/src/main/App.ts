import readline from 'readline'
import { AppModel } from './AppModel';
import { RandomGenerator } from './RandomGenerator';

const model = new AppModel(new RandomGenerator());

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const runLoop = (model: AppModel, rl: readline.Interface)=>{
  rl.on('line', function(line){ 
    if (model.isCompleted() == false) { 
      rl.close();
    } 
    console.log(model.flushOutput());
    model.processInput(line);
    rl.prompt() 
    
  }); 

  rl.on('close', function() { process.exit(); });

}
    
runLoop(model, rl);
