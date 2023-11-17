# sgu-chat
@startuml
!theme cerulean-outline
title SGU-CHAT
skinparam actorStyle awesome
left to right direction
:Пользователь: as user
:Гость: as guest
:Администратор: as admin
rectangle website {
    user --> (Авторизоваться)
    (Авторизоваться) ..> (Отредактировать профиль) : extend
    (user) --> (Подключить платную подписку)
    (Подключить платную подписку) <.. (Отменить подписку) : include
    (Подключить платную подписку) ..> (Слушать посты озвученные AI) : extend
    (user) --> (Опубликовать пост) 
    (Опубликовать пост) ..> (Редактировать пост) : extend
    guest --> (Зарегистрироваться)
    guest --> (Просмотреть посты)
    admin --> (Заблокировать пользователя)
    admin --> (Удалить пост)
}
@enduml
