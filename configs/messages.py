config = {
    "start": """🫶 Привет!
Я бот для исполнения желаний 🧞‍♂️, и меня зовут <b>ВиЛи</b>


<b>👀 Как я работаю?</b>

Ты можешь добавлять в свой список желаний разные вещи которые хочешь, чтобы тебе подарили, или поступки которые хочешь чтобы сделали

Любой кто подпишется на тебя - будет видеть твои желания, а взаимная подписка позволит их исполнять!

Рассказать подробнее? Напиши /help
""",

    "help": """<b>✍️ Как добавить желание?</b>

Введи команду /wish
Затем ты сможешь выбрать категорию, по умолчанию это:

    <b>{light_category}</b>
    
    <b>{medium_category}</b>
    
    <b>{hard_category}</b>
    
Введи название, и дополнительно (но не обязательно) описание - куда можешь добавить ссылку, чтобы подарок было проще найти, описание или что угодно!


<b>🎁 Как исполнять желание?</b>

Введи команду /subscribe
Теперь пришли мне имя пользователя, ИЛИ контакт (в профиле друга выбери "поделиться контактом" и пришли мне), ИЛИ просто перешли любое сообщение от того, на кого хочешь подписаться!

Когда твой друг будет добавлять желание - тебе придет уведомление

Так же ты можешь посмотреть какие есть желания у своих друзей, введя команду /friends

Если твой друг так же подпишется на тебя - вы сможете выполнять желания друг друга! То есть, если ты захочешь выполнить чье-то желание и начнешь его выполнять, другой человек уже не сможет его выполнить - зачем два одинаковых подарка?

Чтобы принять желание к исполнению выбери категорию, желание, и нажми "Хочу исполнить" (будет доступно только если еще никто не выполняет это желание, и если друг на тебя тоже подписан)

А теперь твори добро - твоему другу будет приятно узнать, что он тебе важен =)

Посмотреть какие желания ты сейчас выполняешь можно командой /accepted


<b>✅ Если желание выполнили, я решил его изменить или сам исполнить свое желание?</b>

Введи команду /wishes - тут ты можешь посмотреть свои желания
Выбери категорию и свое желание

Тут ты можешь изменить его, после изменения твои друзья получат об этом уведомление - чтобы быть в курсе твоих интересов

Так же ты можешь выбрать пункт "Удалить" - если твое желание выполнили, если больше не хочешь этого, или если решил сам выполнить желание.
Если кто-то из друзей принял твое желание к исполнению - ты увидишь предупреджение, что желание выполняется, и сможешь выбрать - желание исполнено, или больше не актуально.
""",

    "wish": """🧞‍♂️<b>Новое желание!</b>

Выбери категорию, в которую добавим желание
""",

    "choose_wish_name": """✍️ Что ты хочешь? Опиши желание коротко, потом сможешь уточнить!

Категория: {wish_category}
    
Текущее название: <b>{wish_name}</b>
    
Текущее описание: <i>{wish_description}</i>
""",

    "wish_description": """👏 Отлично!

Теперь можешь написать описание (подробности сюрприза, ссылку на предмет или что угодно!)

Либо, если описание не нужно, нажми {accept} на клавиатуре ниже

Категория: {wish_category}
    
Текущее название: <b>{wish_name}</b>
    
Текущее описание: <i>{wish_description}</i>
""",

    "cancel": """❌ Текущее действие сброшено
""",

    "wrong_symbols": """‼️ Пожалуйста, не используйте в тексте специальные символы, например {{ }}
""",

    "saved_wish": """✅ 🎁 Ваше желание <b>{wish_name}</b> сохранено в категории <b>{wish_category}</b>!

<b>{wish_name}</b>

<i>{wish_description}</i>
""",

    "subscribe": """🫂 <b>Новый друг!</b>

Чтобы увидеть чьи-то желания пришли мне:

Имя пользователя (например, @Vunrir_Beloborod)

ИЛИ

Перешли мне любое сообщение от этого пользователя

ИЛИ

Зайди в его профиль, зайди в меню (три точки сверху), выбери "Поделиться контактом" и пришли мне его контакт
""",

    "cant_subscribe": """❗️ Этот пользователь не использует ВиЛи =(
    
Вы можете посоветовать ему присоединиться, и попробовать еще раз
""",

    "subscribe_friend": """💕 Пользователь <a href="tg://user?id={user_id}">{f_n} {l_n}</a> тоже подписан на Вас - теперь вы можете исполнять желания друг друга!

Так же Вы можете видеть его желания, и будете получать уведомления при появлении новых
""",

    "subscribe_any": """💖 Вы подписаны на <a href="tg://user?id={user_id}">{f_n} {l_n}</a> и можете видеть его желания, а так же будете получать уведомления при появлении новых
    
Чтобы Вы смогли исполнять желания - этот пользователь должен так же подписаться на Вас
""",

    "subscribe_private": """🤍 Вы подписались на <a href="tg://user?id={user_id}">{f_n} {l_n}</a>, но у этого пользователя закрытый профиль =(
    
Вы сможете видеть желания этого пользователя только когда он подпишется на Вас
""",

    "new_wish": """📣 Новое (или измененное) желание от <a href="tg://user?id={user_id}">{f_n} {l_n}</a>
    
<b>{wish_name}</b> в категории {wish_category}

<i>{wish_description}</i>
""",

    "wish_expired": """❌ Это желание уже выполнено, принято к выполнению или удалено
""",

    "wish_execute": """✅ Желание принято к исполнению!

Желание от <a href="tg://user?id={user_id}">{f_n} {l_n}</a>
    
<b>{wish_name}</b>

<i>{wish_description}</i>

Посмотреть принятые к исполнению желания: /accepted
""",

    "max_subscribes": """🔢 ❌ Вы достигли лимита подписок ({cnt})
""",

    "choose_category": """💟 Выбери категорию
""",

    "empty_category": """🔎 Эта категория пуста!
""",

    "look_wishes": """🎁 Ваши желания ({wish_category})

{wish_name}

{wish_description}

_________
Посмотреть желание | Удалить | Редактировать | Выполнено   
""",
    "accept_delete": """
Вы уверены, что хотите удалить желание?

{wish_category}

<b>{wish_name}</b>

<i>{wish_description}</i>

<span class="tg-spoiler">{executing}</span>
""",

    "wish_deleted": """🗑 Желание удалено

<a href="tg://user?id={user_id}">{f_n} {l_n}</a>

{wish_category}

<b>{wish_name}</b>

<i>{wish_description}</i>
""",
    "accept_realize": """
Желание было выполнено?

{wish_category}

<b>{wish_name}</b>

<i>{wish_description}</i>

<span class="tg-spoiler">{executing}</span>
""",

    "wish_realized": """🌟 Желание выполнено!

<a href="tg://user?id={user_id}">{f_n} {l_n}</a>

{wish_category}

<b>{wish_name}</b>

<i>{wish_description}</i>
""",

    "look_accepted_wishes": """🎁 Желания которые Вы выполняете
    
<a href="tg://user?id={user_id}">{f_n} {l_n}</a>

{wish_category}

<b>{wish_name}</b>

<i>{wish_description}</i>

_________
Посмотреть желание | Отказаться   
""",

    "friends_list": """🫂 Ваши друзья
    
_________
Посмотреть желания | Отписаться
""",

    "friend_private": """🔐 У друга <a href="tg://user?id={user_id}">{f_n} {l_n}</a> приватный аккаунт =(
    
Это значит, что просматривать и выполнять его желания могут только те, на кого этот пользователь сам подписан.
Попросите его подписатсья на Вас, чтобы выполнять его желания!
""",

    "friend_categories": """👀🧞‍♂️ Какие желания <a href="tg://user?id={user_id}">{f_n} {l_n}</a> интересуют?
    
_________
Посмотреть желания
""",

    "friend_wishes": """👀🎁 Какое желания <a href="tg://user?id={user_id}">{f_n} {l_n}</a> интересует?

<b>{wish_name}</b>

<i>{wish_description}</i>

<span class="tg-spoiler">{executing}</span>
_________
Посмотреть желание | Исполнять или отказаться
""",

    "friend_delete": """❌ Вы хотите отписаться от пользователя <a href="tg://user?id={user_id}">{f_n} {l_n}</a>?
""",

    "friend_deleted": """❌ Вы отписались от пользователя <a href="tg://user?id={user_id}">{f_n} {l_n}</a>
""",

    "friend_already_deleted": """❌ Вы уже отписались от пользователя <a href="tg://user?id={user_id}">{f_n} {l_n}</a>
""",

    "private_true": """🗝 Ваш аккаунт теперь приватный!

Пользователи смогут видеть Ваши желания только если вы будете подписаны друг на друга
""",

    "private_false": """🗣 Ваш аккаунт теперь публичный!
    
Любой пользователь подписанный на Вас может видеть Ваши желания

<b>ВАЖНО</b>: выполнять желания могут только те пользователи, на которых Вы тоже подписаны
""",

    "too_long_name": """❌ Это имя слишком длинное!

Пожалуйста, задайте имя короче (не более 30 символов), позже Вы сможете добавить описание и подробнее расписать желание
""",

    "too_long_description": """❌ Это описание слишком длинное!

Пожалуйста, задайте описание короче (не более 2000 символов)
""",

    "old_message": """😔 Это сообщение устарело
""",

    "already_subscribe": """🫂 Вы уже подписаны на этого пользователя
""",

    "not_subscriber_friend": """🔐 Этот друг <a href="tg://user?id={user_id}">{f_n} {l_n}</a> не полписан на Вас =(

Попросите его подписатсья на Вас, чтобы выполнять его желания!
""",
}

