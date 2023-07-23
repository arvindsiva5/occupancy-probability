def select_sections(occupancy_probability: list[list[int]]) -> list:
    """
    Function description: Choose n sections in an office floor with m columns and n rows such that
                          the n sections total up to the minimum possible total occupancy probability compared
                          to selecting other n sections. These n sections, each row 1 section is selected and
                          and each section above or below the selected section in a row must be in the same
                          or adjacent column.

    Approach description: 
    To solve this problem dynammic programming is used by breaking the problem into smaller sub problems then
    combine the solutions of these sub problems to get the solution to the problem. To achive these base cases
    are needed (small problems that have a defined solution). In this case, if the office floor had only 1
    row and multiple columns then only 1 section in this row would give us the minimum total occupancy. If we look
    closer at every column in that one row, the minimum total occupancy if that column was the last section to 
    be selectected is the occupancy rate of that column becuase there is just 1 row. So using this as a base case
    we can find such that for selecting any (i,j) (row, column) [i is 0...n-1, j is 0...m-1] in the floor as the 
    last section of n sections is the minimum total probability if (i,j) is the last section. By doing this we find 
    the minimum (n-1, j) in the last row j and that would be the minimum total occupancy rate for n sections 
    selected in the whole floor.
    
    In building the reccurence relation to this problem the condition that if any (i, j) section is selected
    the section selected before it (row above) must have the same or diagonal column of (i, j) which means
    the previous row selected section must be the minimum of (i-1, j-1), (i-1,j) and (i-1, j+1). This will
    ensure that the minimum total occupancy rate if (i, j) is the last selected section can be computed accurately.
    By making use of this the recurence relation below whuch makes use of dynamic programming is created:
    
    , where occupancy_probability[i][j] is the occupancy probability at section (i,j)
    , where memo[i][j] is the minimum total occupancy probability if section (i,j) is the last selected section
    , where i is 0...n-1 (n rows)
    , where j is 0...m-1 (m columns)

    if i = 0
    memo[i][j] = occupancy_probability[i][j]

    if i > 0 && j > 0 && j < m-1
    memo[i][j] = occupancy_probability[i][j] + max(memo[i-1][j-1], memo[i-1][j], memo[i-1][j+1])

    if i > 0 && j = 0
    memo[i][j] = occupancy_probability[i][j] + max(memo[i-1][j], memo[i-1][j+1])

    if i > 0 && j = m-1
    memo[i][j] = occupancy_probability[i][j] + max(memo[i-1][j-1], memo[i-1][j])
    
    n sections with minimum total occupancy probability will be the minimum of memo[n-1][0...m-1]

    The time complexity is O(nm), where n is the number of rows (number of lists in the list) in 
    occupancy_probability & m is the number of columns (number of integers in each list) in occupancy_probability.
    This is because the 2 for loops the outer one loops n times and the inenr one loops m times with constant time
    operations within it making it O(nm) all together. This dominates O(m) needed to copy the first row. 
    The creation of memo and pred is also O(nm). O(nm) still dominates the O(n+m) needed by select_sections_ret. 
    Hence, the time complexity of the function is O(nm). The space created when creating memo and pred is O(nm).
    O(nm) dominates the space created by select_sections_ret of O(n). Hence the Auxilary space complexity 
    is O(nm).

    :Input:
        occupancy_probability: A list of lists. There are n interior lists. All interior lists are length m
        (columns/aisles). Each interior list represents a different row of sections. occupancy_probability[i][j]
        is an integer number between 0 and 100 (inclusive) which represents the occupancy probability
        for a section located at row i and column/aisle j
    :Output:
        A list with an integer and another list, where the integer is the total occupancy for the selected n
        sections to be removed and the list consist of n tuples in the form of (i, j). Each tuple represents
        the location of one section selected for removal. i refers to the row index and can range from
        0 to n - 1. j refers to the column index and can range from 0 to m - 1.
    :Time complexity: O(nm), where n is the number of rows (number of lists in the list) in occupancy_probability
                           , where m is the number of columns (number of integers in each list)
                             in occupancy_probability
    :Aux space complexity: O(nm), where n is the number of rows (number of lists in the list)
                                  in occupancy_probability
                                , where m is the number of columns (number of integers in each list)
                                  in occupancy_probability
    """
    n = len(occupancy_probability)  # number of rows n
    m = len(occupancy_probability[0])   # number of columns m

    # memo stores the minimum total occupancy rate if (i, j) is the last selected section
    memo = [[0 for _ in range(m)] for _ in range(n)]
    memo[0] = occupancy_probability[0].copy()

    # stores the predescesor selected in the row before (above row) for each (i, j)
    pred = [[None for _ in range(m)] for _ in range(n)]

    for i in range(1, n):   # loops 2nd row to last row
        for j in range(m):  # loops every column
            # get the minimum occupancy probability to select in row above and the index
            min = get_min(i, j, m, memo)

            # add the minimum occupancy probability from row above and store the index as the predescesor
            memo[i][j] = min[0] + occupancy_probability[i][j]
            pred[i][j] = min[1]

    # using memo and pred the list of n sections with the minimum total occupancy rate is computed
    # the minimum_total_occupancy & sections_location is returned
    return select_sections_ret(memo, pred)


def get_min(i: int, j: int, m: int, memo: list[list[int]]) -> list:
    """
    Function description: Gets the minimum occupancy rate to select at the row above section (i,j) in
                          occupancy_probability to be selected and added to (i,j) in memo to achieve the
                          minimum total occupancy probability if location (i,j) was the last selected
                          section. Also returns the index of the selected minimum occupancy rate from
                          the row above. Only considers sections in row above with same or diagonal 
                          column for finding the minimum from row above.

    :Input:
        i: An integer representing the row
        j: An integer representing the column
        m: An integer representing the number of columns in the occupancy probability list
        memo: A list of list of integers representing the minimum total occupancy probability 
              if section (i,j) is the last selected section

    :Output:
        A list of an integer and a tuple of two integers, the integer reprsents the minimum probability value
        to be selected from the row above min_total_probability[i][j] diagonaly and vertically and the tuple
        of two integers (x,y) reprsent the index position of the minimum probability value to be selected in
        min_total_probability
    :Time complexity: O(1)
    :Aux space complexity: O(1)
    """

    probability = []    # stores probabilies of valid sections to be selected from row above
    probability_index = []  # stores index of valid sections to be selected from row above

    # select the section from row above with same column
    probability.append(memo[i - 1][j])
    probability_index.append((i - 1, j))

    # select the section from row above with left adjacent column if j not first column
    if j > 0:  
        probability.append(memo[i - 1][j - 1])
        probability_index.append((i - 1, j - 1))

    # select the section from row above with right adjacent column if j not last column
    if j < m - 1:
        probability.append(memo[i - 1][j + 1])
        probability_index.append((i - 1, j + 1))

    # set the first section in selected list as minimum
    min = probability[0]
    ind = probability_index[0]

    # find the section from row above with minimum occupancy probability and its index
    for i in range(len(probability)):
        if probability[i] < min:
            min = probability[i]
            ind = probability_index[i]

    # returns the minimum occupancy probability and its index
    return (min, ind)


def select_sections_ret(memo: list[list[int]], pred: list[list[int]]):
    """
    Function description: Using memo and the predescesors in pred the minimum_total_occupancy and sections_location
                          is computed by selecting the smallest minimum total occupancy at the last row, row n 
                          as the minimum_total_occupancy and use its predescessors to find the n-1 sections 
                          before it that adds up to the minimum_total_occupancy to find the sections_location and 
                          the minimum_total_occupancy and sections_location is returned.

    :Input:
        memo: A list of list of integers representing the minimum total occupancy probability 
              if section (i,j) is the last selected section
        pred: A list of lists with tuples (i, j), pred is size m*n, the tuple (i, j) at every position
              represents the index of the minimum probability in the row above it that was selected 
              (vertically or diagonally). The first list in the list of lists (first row) is filled with None
              because they are the starting minimum probabilities (the base cases)
    :Output:
        A list consisting an integer minimum_total_occupancy and a list sections_location
        , where minimum_total_occupancy is an integer, which is the total occupancy for the selected n
          sections to be removed
        , where sections_location is a list of n tuples in the form of (i, j). Each tuple represents the
          location of one section selected for removal. i refers to the row index and can range from
          0 to n - 1. j refers to the column index and can range from 0 to m - 1.
    :Time complexity: O(n + m), where n is the number of lists in min_total_probability (number of rows)
                              , where m is the number of columns (number of integers in each list) 
                                in occupancy_probability
    :Aux space complexity: O(n), where n is the number of lists in min_total_probability (number of rows)
    """
    n = len(memo)   # number of rows
    minimum_total_occupancy = min(memo[n - 1])  # the minimum total occupancy probability for n sections
    # index of section in last row for the minimum total occupancy probability for n sections
    ind = (
        len(memo) - 1,
        memo[n - 1].index(minimum_total_occupancy),
    )
    # list of n sections to be selected for the minimum total occupancy probability for n sections
    sections_location = [ind]

    # loops till the 1st row and append the selected sections index in reverse
    while ind != None:
        sections_location.append(pred[ind[0]][ind[1]])
        ind = pred[ind[0]][ind[1]]

    # the first row would have no predescessor and None is appended
    # the None is removed here
    sections_location.pop(len(sections_location) - 1)

    # the list of n sections is reversed to for correct order (first row to n-th row)
    sections_location.reverse()

    # minimum_total_occupancy and sections_location is returned
    return [minimum_total_occupancy, sections_location]
