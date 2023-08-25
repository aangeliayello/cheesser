# CHEeSSer
p/q2-q4!

## Bugs:
- [['r' '_' 'b' 'q' 'k' '_' 'n' 'r']
 ['p' 'p' 'p' 'p' '_' '_' '_' 'p']
 ['_' '_' '_' 'N' '_' '_' 'p' '_']
 ['_' '_' 'n' 'P' '_' '_' '_' '_']
 ['_' '_' '_' 'R' 'p' '_' '_' '_']
 ['P' '_' '_' '_' 'B' '_' '_' '_']
 ['_' 'P' 'P' '_' '_' 'P' 'P' 'P']
 ['_' '_' 'K' '_' '_' 'B' 'N' 'R']]
## TODO:
     General:
     - Set up performance measures
     
     Game:
     - Implement En pasant in move generation
     - Implement Casling in move generation
     - Implement check for check

     Game Play:
     - update incentive heatmap
     - bot keeps computing while human thinks
     
     Speed:
     - Pre calculate tables
          - Implement simple fast update of hash
     - Vectorize
     - Parallelize

     UX:
     - Move input and output should be in [A-H][1-8] notation
     - fix wrong move bug
     - validade human moves
     - chose color to play
     - back tracking 
     - saving of games
     - implement ui to play
     
     Interface:
     - Connect to Lichess 
     - implement bot language protocol
