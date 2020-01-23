# Симулятор робота, перемещающегося по полю

## Архитектура приложения

### Класс Robot:

Класс Robot спроектирован таким образом, что его позиция движение и повороты осуществляются на плоскости Декартовой системы координат.

#### Атрибуты:

* position - содержит в себе координаты x, y позиции робота на плоскости в Декаровой системе координат;
* direction - содержит в себе единичный вектор, указывающий напрвление поворота робота;
* color - цвет робота при отрисовке на игровом поле;
* rotated_up, rotated_down, rotated_left, rotated_right - шаблоны для отрисовки робота в зависимости от поворота робота.

#### Методы:

* get_position() - возвращает координаты x, y позиции робота;
* get_direction() - возвращает вектор, указывающий направление поволота робота;
* get_body() - возвращает шаблон для отрисовки робота в зависимости от его направления.
* move() - робот делает шаг в зависимости от его направления путём сложения координат текущей позиции робота и координат вектора его направления;
* rotate() - в зависимости от поданного в качестве аргумента числа -1, 1 или 0, поворачивает робота соответственно направо на 90, налево на 90 и разворачивает на 180 градусов соответственно.


### Класс Game: 

Класс Game спроектирован таким образом, что при его инициализации можно задать ширину и высоту игрового поля, игровое поле из файла (в зависимости от режима игры) и количество препятствий на игровом поле

#### Атрибуты:

* robot - содержит в себе экземпляр класса Robot;
* width, height - ширина и высота игрового поля соответственно;
* center - центр игрового поля откуда начинает своё движение робот;
* last_command - содержит в себе последнюю команду, принятую от пользователя;
* error_message - содержит в себе текст ошибки, возникшей в процессе игры;
* commands - содержит в себе все команды пользователя, принятые в процессе игры;
* obstacles_count - содержит в себе количество препятсвий, которые нужно расположить на игровом поле;
* field - содержит в себе игровое поле. В зависимости от режима загружается из файла или формируется заново.

#### Методы:

* normalize_position() - принимает на вход в качестве аргумента координаты точки и возвращает индекс игрового поля;
* get_robot_body_idx() - возвращает список индексов робота на игровом поле;
* get_rotate_direction - возвращает направление, в которое нужно повернуть робота;
* get_area_indexes() - возвращиет список индексов вокруг центральной точки, поданной в качестве атрибута, в некоторого размера, поданного в качестве атрибута;
* set_wall() - устанавливает стену на игровом поле по его периметру;
* set_obstacles() - устанавливает препятствия на игровом поле;
* render() - отрисовывает сформированное игровое


