occupancy_probability is a list of lists. There are n interior lists. All interior lists are length m (columns/aisles). Each interior list represents a different row of sections. occupancy_probability[i][j] is an integer number between 0 and 100 (inclusive) which represents the occupancy probability for a section located at row i and column/aisle j.

select_sections(occupancy_probability) is a function that chooses n sections in an office floor with m columns and n rows such that the n sections total up to the minimum possible total occupancy probability compared to selecting other n sections. These n sections, each row 1 section is selected and each section above or below the selected section in a row must be in the same or adjacent column.

select_sections() will return a list of 2 items:\
• minimum_total_occupancy is an integer, which is the total occupancy for the selected n sections to be removed\
• sections_location is a list of n tuples in the form of (i, j). Each tuple represents the location of one section selected for removal. i refers to the row index and can range from 0 to n − 1. j refers to the column index and can range from 0 to m − 1.\

Example:\
occupancy_probability = [[31, 54, 94, 34, 12], [26, 25, 24, 16, 87], [39, 74, 50, 13, 82], [42, 20, 81, 21, 52], [30, 43, 19, 5, 47], [37, 59, 70, 28, 15], [ 2, 16, 14, 57, 49], [22, 38, 9, 19, 99]]\
select_sections(occupancy_probability)\
\>>> [118, [(0, 4), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 2), (7, 2)]]
