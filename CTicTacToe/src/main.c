#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

char BOARD[10] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};

void DisplayBoard();
void ClearBoard();
void PlayTurn(const char marker);
bool MarkBoard(const unsigned short position,const char marker);
bool IsPositionFilled(const unsigned short position);
bool IsGameOver();

int main() {
  unsigned short turn_count = 0;

  while (!IsGameOver() && ++turn_count <= 9) {
    PlayTurn((turn_count % 2 == 0) ? 'O' : 'X');
  }

  ClearBoard();
  printf("GAME OVER\n\n");
  DisplayBoard();

  return 0;
}

inline void DisplayBoard() {
  printf("Tic Tac Toe\nPlayer 1: X\nPlayer 2: O\n\n");
  printf(" %c | %c | %c \n", BOARD[7], BOARD[8], BOARD[9]);
  printf("-----------\n");
  printf(" %c | %c | %c \n", BOARD[4], BOARD[5], BOARD[6]);
  printf("-----------\n");
  printf(" %c | %c | %c \n", BOARD[1], BOARD[2], BOARD[3]);
}

inline void ClearBoard() {
  system("clear");
}

void PlayTurn(const char marker) {
  static unsigned short position;
  do {
    TURN_START: ClearBoard();
    DisplayBoard();
    printf("\nPlayer %c's turn. Enter a position: ", marker);
    scanf("%hu", &position);
    if (position < 1 || position > 9) {
      goto TURN_START;
    }
  } while (!MarkBoard(position, marker));
}

bool MarkBoard(
    const unsigned short position,
    const char marker) {
  static bool successful = true;
  if (IsPositionFilled(position)) {
    successful = false;
  } else {
    successful = true;
    BOARD[position] = marker;
  }
  return successful;
}

bool IsPositionFilled(
    const unsigned short position) {
  static char marker;
  static bool is_filled = false;
  marker = BOARD[position];
  if (marker == 'X' || marker == 'O') {
    is_filled = true;
  } else {
    is_filled = false;
  }
  return is_filled;
}

bool IsGameOver() {
  static bool game_over = false;
  if (BOARD[1] == BOARD[2] && BOARD[2] == BOARD[3]) {
    game_over = true;
  } else if (BOARD[4] == BOARD[5] && BOARD[5] == BOARD[6]) {
    game_over = true;
  } else if (BOARD[7] == BOARD[8] && BOARD[8] == BOARD[9]) {
    game_over = true;
  } else if (BOARD[1] == BOARD[4] && BOARD[4] == BOARD[7]) {
    game_over = true;
  } else if (BOARD[2] == BOARD[5] && BOARD[5] == BOARD[8]) {
    game_over = true;
  } else if (BOARD[3] == BOARD[6] && BOARD[6] == BOARD[9]) {
    game_over = true;
  } else if (BOARD[1] == BOARD[5] && BOARD[5] == BOARD[9]) {
    game_over = true;
  } else if (BOARD[3] == BOARD[5] && BOARD[5] == BOARD[7]) {
    game_over = true;
  }
  return game_over;
}
