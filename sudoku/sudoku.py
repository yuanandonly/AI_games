import sys, time
start = time.time()
#sets up board structure and references
numbers = '123456789'
sections = ['123', '456', '789']
cells = [a + b for a in numbers for b in numbers]
rows = dict((num, [num + a for a in numbers]) for num in numbers)
columns = dict((num, [a + num for a in numbers]) for num in numbers)
grids = []
for A in sections:
  for B in sections:
    grids.append([a + b for a in A for b in B])
# list of rows, columns, and grids which all have to contain 1-9
constraints = grids + [v for k, v in rows.items()] + [q for p, q in columns.items()]
# dictionary that maps a cell value to a set containing the cells in the 
# row, column, and grid that it belongs to
neighbors = dict((u, set(set(rows[u[0]]).union(set(columns[u[1]])))) for u in cells)
for g in grids:
  for e in g:
    neighbors[e] = neighbors[e].union(set(g))

def brute(pzl, ind, values):
  v_check = [v for k, v in pzl.items()]
  if v_check.count('.') == 0:
  # i = checkinc(pzl, ind)
  # if i == 2:
    return pzl
  # elif i == 1:
  else:
    minpos = 9
    minsym = 9
    pos = []
    sym = []
    val = 0
    #constrained cell
    for k, v in values.items():
      if pzl[k] == '.' and len(v) < minpos and len(v) > 0:
        pos = [k]
        minpos = len(v)
        if minpos == 1:
          break
      elif v == '.' and len(v) == minpos:
        pos.append(k)



    if minpos > 1:
      #constrained symbol
      for j in constraints:
        for i in '123456789':
          if minsym > 1:
            poss = [k for k in j if pzl[k] == '.' and i in values[k]]
            length = len(poss)
            if length < minsym and len(poss) > 0:
              sym = poss
              val = i
              minsym = length
    resetp = dict(values)
    #constrain symbol
    if minsym < minpos:
      for x in sym:
        pzl[x] = val
        values[x] = val
        for n in neighbors[x]:
          values[n] = values[n].replace(val, '')
        p = brute(pzl, x, values)
        # print(p)
        if p:
          return pzl
        pzl[x] = '.'
        values = resetp 
    #constrain cell
    else:
      for x in pos:
        a = values[x]
        #a = set(numbers).difference(set([pzl[n] for n in neighbors[x]]))
        for b in a:
          pzl[x] = b
          values[x] = b
          for n in neighbors[x]:
            values[n] = values[n].replace(b, '')
          p = brute(pzl, x, values)
          #print(p)
          if p:
            return pzl
          pzl[x] = '.'
          values = resetp
  return ""

def checkinc(pzl, index):
  values = [v for k, v in pzl.items()]
  if values.count('.') == 0:
    return 2
  return 1

def display(valuesa, valuesb):
  print("____________________________________________")
  width = 1+max(len(valuesa[u]) for u in cells)
  line = '+'.join(['-'*(width*3)]*3)
  for a in numbers:
    print(''.join(valuesa[a+b].center(width)+('|' if b in '36' else '') for b in numbers) + "  >  " + ''.join(valuesb[a+b].center(width)+('|' if b in '36' else '') for b in numbers))
    if a in '36':
      print(line + "  >  " + line)

def readfile(filename):
  with open(filename) as f:
    content = f.readlines()
  content = [x.strip() for x in content]
  return content

def main():
  #file
  puzzles = readfile("puzzlesHarder.txt")
  for puzz in range(len(puzzles)):
    values = dict((c, '123456789') for c in cells)
    puzzle = {}
    for j in range(len(cells)):
      puzzle[cells[j]] = puzzles[puzz][j]
    # for all the given values in the original puzzle, removes that value from
    # the possible values of each of its neighbor cells  
    for k, v in puzzle.items():
      if v != '.':
        for neigh in neighbors[k]: 
          values[neigh] = values[neigh].replace(v, '')
    solution = brute(dict(puzzle), '11', values)
    if solution:
      display(puzzle, solution)
    print(puzz + 1)
    puzz += 1
  print("____________________________________________")
  final = time.time() - start
  print(final, "seconds total")

if __name__ == '__main__':
  main()