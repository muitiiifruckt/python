$(document).ready(function() {
    function createChessBoard() {
        const board = document.getElementById('chessboard');
        // Убедитесь, что board не null
        if (!board) {
            console.error('Chessboard element not found');
            return;
        }
            for (let i = 0; i < 64; i++) {
        const square = document.createElement('div');
        const isBlack = (Math.floor(i / 8) + i) % 2 === 0;
        square.className = isBlack ? 'black' : 'white';

        // Вычисляем координаты
        const x = 'abcdefgh'[i % 8];
        const y = 8 - Math.floor(i / 8);
        square.setAttribute('data-coord', `${x}${y}`);

        board.appendChild(square);
    }

            // Функция для добавления фигуры на доску
    function addPiece(piece, position) {
        const pieceElement = document.createElement('img');
        pieceElement.src = '/static/figures/' + piece + '.png';
        pieceElement.className = 'chesspiece';
        pieceElement.draggable = true;

        // Вычисляем координаты
        const x = 'abcdefgh'[position % 8];
        const y = 8 - Math.floor(position / 8);
        const coord = `${x}${y}`;

        // Устанавливаем id фигуры на основе её позиции
        const pieceId = `${piece}-${coord}`;
        pieceElement.id = pieceId;

        // Устанавливаем атрибут data-coord для фигуры
        pieceElement.setAttribute('data-coord', coord);

        board.children[position].appendChild(pieceElement);
    }


        const pieces = ['pawn_white', 'pawn_black', 'rook_white', 'knight_white', 'bishop_white', 'queen_white', 'king_white', 'bishop_white', 'knight_white', 'rook_white', 'rook_black', 'knight_black', 'bishop_black', 'queen_black', 'king_black', 'bishop_black', 'knight_black', 'rook_black'];

        // Расстановка фигур на доске
        // Белые пешки
        for (let i = 8; i < 16; i++) {
            addPiece('pawn_white', i);
        }
        // Черные пешки
        for (let i = 48; i < 56; i++) {
            addPiece('pawn_black', i);
        }
        // Остальные фигуры
        addPiece('rook_white', 0);
        addPiece('knight_white', 1);
        addPiece('bishop_white', 2);
        addPiece('queen_white', 3);
        addPiece('king_white', 4);
        addPiece('bishop_white', 5);
        addPiece('knight_white', 6);
        addPiece('rook_white', 7);
        addPiece('rook_black', 56);
        addPiece('knight_black', 57);
        addPiece('bishop_black', 58);
        addPiece('queen_black', 59);
        addPiece('king_black', 60);
        addPiece('bishop_black', 61);
        addPiece('knight_black', 62);
        addPiece('rook_black', 63);

        let draggedElement = null;
        document.querySelectorAll('.chesspiece').forEach(piece => {
            piece.addEventListener('dragstart', (e) => {
                draggedElement = e.target;
                e.target.style.opacity = '0.1'; // Делаем фигуру полупрозрачной при перетаскивании
                // Подсветка возможных ходов или клеток может быть добавлена здесь
                e.dataTransfer.setDragImage(e.target, 75/2, 75/2);

            });

            piece.addEventListener('dragend', (e) => {
                e.target.style.opacity = ''; // Возвращаем нормальную прозрачность фигуре
                // Убираем подсветку клеток

            });
        });


         document.querySelectorAll('#chessboard div').forEach(square => {
        square.addEventListener('drop', (e) => {
            e.preventDefault();
            console.log(1);

            const targetSquare = e.target.closest('.black, .white');
            console.log(1);
            if (draggedElement && targetSquare) {
                while (targetSquare.firstChild) {
                    targetSquare.removeChild(targetSquare.firstChild); // Удаляем фигуру с клетки, если таковая имеется
                }
                targetSquare.appendChild(draggedElement); // Помещаем перетаскиваемую фигуру на клетку

                // Запоминаем исходные и конечные координаты
                const fromCoord = draggedElement.getAttribute('data-coord');
                const toCoord = targetSquare.getAttribute('data-coord');

                // Сбрасываем ссылку на перетаскиваемый элемент
                draggedElement.style.opacity = ''; // Возвращаем нормальную прозрачность фигуре
                draggedElement = null;
                console.log(1);
                // Отправляем данные о ходе на сервер через AJAX
                $.ajax({
                    url: '/make_move', // URL, на который будет отправлен запрос
                    type: 'POST',
                    data: {
                        from: fromCoord,
                        to: toCoord,
                        // Можно добавить дополнительные данные, если необходимо
                    },
                    success: function(response) {
                    if(response.move_made) {
                        console.log(response.message); // Отображаем сообщение об успешном выполнении хода
                        // Можете добавить логику для обновления UI здесь
                    } else {
                        alert(response.message); // Эта ветка не будет выполняться, пока используется заглушка
                    }
                },

                    error: function(xhr, status, error) {
                        // Здесь вы можете обработать ошибки запроса
                        // Например, вывести сообщение об ошибке
                    }
                });
            }
        });
    });
    }

    createChessBoard();
});
