from grid import *

def main(screen, width):
    rows = 50
    grid = make_grid(rows, width)

    start_node = None
    end_node = None

    running = True
    started = False

    while running:  #main loop
        draw(screen, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:   #lmb
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, rows, width)
                node = grid[row][col]

                if not start_node and node != end_node:
                    start_node = node
                    start_node.make_start()

                elif not end_node and node != start_node:
                    end_node = node
                    end_node.make_end()

                elif node != end_node and node != start_node:
                    node.make_obst()


            elif pygame.mouse.get_pressed()[2]: #rmb
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, rows, width)
                node = grid[row][col]

                if node.color != RED and node.color != BLUE:
                    node.reset()
                if node == start_node:
                    start_node = None

                if node == end_node:
                    end_node = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started: #run A* algorithm
                    for row in grid:
                        for node in row:

                            node.update_neighbors(grid)
                    a_star(lambda: draw(screen, grid, rows, width), grid, start_node, end_node)

                if event.key == pygame.K_r:
                    start_node = None
                    end_node = None
                    grid = make_grid(rows, width)

    pygame.quit()

main(screen,800)    #run main function with a screen width of 800