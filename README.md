# calculator compiler

## About

You can compile commands and calculate some mathematic logics !

## Commands

| Operation | Description                                   |
| --------- | --------------------------------------------- |
| +         | Plus expression's results together            |
| =         | Assign an expression's result into a variable |
| -         | Mines expression's results together           |
| \*        | Multiply expression's results together        |
| /         | Division expression's results together        |
| ^         | Power expression's results together           |
| ()        | Open and close bracket                        |
| print     | print an expression's result or a variable    |

> You are free to use **variables**

## Usage

```bash
python ./Syntax_Analyzer.py [FILE_PATH]
```

## Example

Sample file content:

```
count = 4  + 4 * (5+6)-7

Count = count + 1

print count-4

x = count * 2^2^2 * (4-2)

print x
count = 3* -x +4/3

print count
```

1. Run

```bash
python ./Syntax_Analyzer.py ./sample/calculator-commands-simple.txt
```

1. Results

```bash
37.0
1312.0
-3934.6666666666665
```
