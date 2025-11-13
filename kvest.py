import os
import time

class GameState:
    def __init__(self):
        self.inventory = []
        self.reputation = 0  # + за добро, - за зло
        self.elf_ally = False
        self.dwarf_ally = False
        self.bandit_ally = False
        self.has_artifact = False
        self.has_shadow_magic = False
        self.has_hammer = False
        self.has_gun_blueprint = False
        self.has_mercenaries = False
        self.has_map = False
        self.saved_prince = False
        self.convinced_captain = False
        self.mortkow_offer = False

game = GameState()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def choice_prompt(options):
    print("\n" + "="*50)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("\nВаш выбор: "))
            if 1 <= choice <= len(options):
                return choice
            else:
                print("Пожалуйста, выберите существующий вариант")
        except ValueError:
            print("Введите число")

def act1_start():
    clear_screen()
    print_slow("АКТ I: ПРОБУЖДЕНИЕ")
    print_slow("\nВы приходите в сознание среди дымящихся руин цитадели Ордена Серебряного Феникса.")
    print_slow("Ваш Магистр, истекая кровью, протягивает вам печать Ордена.")
    print_slow('"Морток... король... предан... Ищи ответы..."')
    print_slow('"Лес... Шахты... Равнины..."')
    print_slow("\nПеред вами три пути:")
    
    choice = choice_prompt([
        "Отправиться в Таинственный Лес Эльфов",
        "Спуститься в Заброшенные Шахты Гномов", 
        "Исследовать Выжженные Равнины"
    ])
    
    if choice == 1:
        return act2_elf_forest()
    elif choice == 2:
        return act2_dwarf_mines()
    else:
        return act2_burned_plains()

def act2_elf_forest():
    clear_screen()
    print_slow("ЛЕС ЭЛЬФОВ")
    print_slow("\nВы входите в древний лес. Воздух звенит магией.")
    print_slow("Эльфийский дозорный появляется из-за деревьев.")
    print_slow('"Человек! Что привело тебя в наши владения?"')
    
    choice = choice_prompt([
        "Показать печать Ордена и попросить помощи",
        "Попытаться пробраться тайком вглубь леса"
    ])
    
    if choice == 1:
        print_slow('\n"Печать Серебряного Феникса... Я помню этот орден."')
        print_slow('"Но доверия нужно заслужить. Наше Лесное Сердце отравлено скверной Мортека."')
        return act3_elf_quest()
    else:
        print_slow("\nВы пытаетесь обойти дозорных, но эльфийская магия обнаруживает вас.")
        print_slow("Вас захватывают и ведут к Королеве Эльфов.")
        return act3_elf_betrayal()

def act3_elf_quest():
    clear_slow("\nКоролева Эльфов взирает на вас с подозрением.")
    print_slow('"Очисти Лесное Сердце от скверны, и мы поможем тебе."')
    
    print_slow("\nВы находите источник порчи - кристалл тьмы, питающийся магией леса.")
    
    choice = choice_prompt([
        "Провести ритуал очищения (собрать три священные травы)",
        "Разрушить кристалл силой оружия"
    ])
    
    if choice == 1:
        print_slow("\nВы собираете Лунный Цветок, Звездную Пыль и Слезу Феникса.")
        print_slow("Ритуал очищения проходит успешно! Лес наполняется светом.")
        print_slow('Королева дарует вам РОГ ЛЕСА - артефакт, призывающий эльфийских лучников.')
        game.elf_ally = True
        game.has_artifact = True
        game.reputation += 2
    else:
        print_slow("\nВы атакуете кристалл, но обратная волна магии ранит вас.")
        print_slow("Эльфы спасают вас, но доверия не прибавляется.")
        game.reputation += 1
    
    return act4_capital()

def act3_elf_betrayal():
    print_slow('\n"Вор и шпион! Ты заплатишь за это!"')
    
    choice = choice_prompt([
        "Попытаться договориться",
        "Сражаться до конца",
        "Украсть эльфийскую реликвию и бежать"
    ])
    
    if choice == 1:
        print_slow("\nВам удается убедить эльфов в своих добрых намерениях.")
        print_slow("Они отпускают вас, но помощи не предлагают.")
        game.reputation -= 1
    elif choice == 2:
        print_slow("\nВы сражаетесь отчаянно, но против магии эльфов нет шансов.")
        print_slow("Вас изгоняют из леса.")
        game.reputation -= 2
    else:
        print_slow("\nПока эльфы спорят о вашей судьбе, вы крадете СФЕРУ ТЕНЕЙ.")
        print_slow("Древний артефакт дает вам доступ к запретной магии.")
        game.has_shadow_magic = True
        game.reputation -= 3
    
    return act4_capital()

def act2_dwarf_mines():
    clear_screen()
    print_slow("ШАХТЫ ГНОМОВ")
    print_slow("\nГорный проход завален камнями. Слышны крики и лязг оружия изнутри.")
    
    choice = choice_prompt([
        "Разобрать завал и помочь гномам",
        "Найти обходной путь через вентиляционные шахты"
    ])
    
    if choice == 1:
        print_slow("\nВы пробиваетесь внутрь и видите гномов, сражающихся с троллями.")
        return act3_dwarf_battle()
    else:
        print_slow("\nОбходной путь ведет в заброшенную мастерскую.")
        return act3_dwarf_workshop()

def act3_dwarf_battle():
    print_slow("\nКороль Гномов кричит: 'Помоги нам, человек, и мы не забудем эту услугу!'")
    
    choice = choice_prompt([
        "Атаковать троллей вместе с гномами",
        "Починить древнюю откачивающую помпу и затопить пещеры троллей"
    ])
    
    if choice == 1:
        print_slow("\nВместе вы побеждаете троллей! Гномы ликуют.")
        print_slow('Король дарует вам ДРЕВНИЙ РУНИЧЕСКИЙ МОЛОТ.')
        game.dwarf_ally = True
        game.has_hammer = True
        game.reputation += 2
    else:
        print_slow("\nВы находите механизм и запускаете его. Тролли тонут в подземных водах.")
        print_slow("Гномы благодарны, но некоторые сомневаются в ваших методах.")
        game.reputation += 1
    
    return act4_capital()

def act3_dwarf_workshop():
    print_slow("\nВ мастерской вы находите чертежи древнего оружия.")
    
    choice = choice_prompt([
        "Вернуть чертежи гномам",
        "Украсть чертеж ОГНЕННОЙ ПУШКИ и уйти незамеченным"
    ])
    
    if choice == 1:
        print_slow("\nГномы восхищены вашей честностью.")
        print_slow("В награду они делятся с вами секретами рунической магии.")
        game.dwarf_ally = True
        game.reputation += 2
    else:
        print_slow("\nВы крадете чертеж и скрываетесь. Теперь у вас есть мощное оружие.")
        print_slow("Но гномы поклялись отомстить.")
        game.has_gun_blueprint = True
        game.reputation -= 2
    
    return act4_capital()

def act2_burned_plains():
    clear_screen()
    print_slow("ВЫЖЖЕННЫЕ РАВНИНЫ")
    print_slow("\nБескрайние пустоши, где выживают только сильнейшие.")
    print_slow("Вы находите лагерь банды 'Вольные Соколы'.")
    
    choice = choice_prompt([
        "Предложить свои услуги бандитам",
        "Напасть на бандитов и забрать их припасы",
        "Обойти лагерь и искать другие пути"
    ])
    
    if choice == 1:
        return act3_bandit_join()
    elif choice == 2:
        return act3_bandit_fight()
    else:
        return act3_bandit_stealth()

def act3_bandit_join():
    print_slow("\nЛидер банды Гаррет оценивающе смотрит на вас.")
    print_slow('"Хочешь присоединиться? Докажи преданность - ограбь королевский караван."')
    
    choice = choice_prompt([
        "Согласиться и участвовать в ограблении",
        "Отказаться и уйти"
    ])
    
    if choice == 1:
        print_slow("\nОграбление проходит успешно! Гаррет доволен.")
        print_slow("Теперь у вас есть ОТРЯД НАЕМНИКОВ для штурма замка.")
        game.bandit_ally = True
        game.has_mercenaries = True
        game.reputation -= 2
    else:
        print_slow("\nГаррет смеется: 'Мягкотелый рыцарь!' Но отпускает вас.")
        game.reputation += 1
    
    return act4_capital()

def act3_bandit_fight():
    print_slow("\nВы нападаете на бандитов. Завязалась жестокая схватка!")
    
    if game.has_hammer or game.has_shadow_magic:
        print_slow("Ваше оружие/магия дают преимущество! Вы побеждаете.")
        print_slow("Среди вещей Гаррета вы находите ТАКТИЧЕСКУЮ КАРТУ патрулей.")
        game.has_map = True
        game.reputation += 1
    else:
        print_slow("Бандитов слишком много! Вам едва удается спастись.")
        game.reputation += 1
    
    return act4_capital()

def act3_bandit_stealth():
    print_slow("\nВы обходите лагерь и находите заброшенный наблюдательный пост.")
    print_slow("Среди бумаг - карты и документы о передвижениях войск Мортека.")
    
    game.has_map = True
    game.reputation += 1
    return act4_capital()

def act4_capital():
    clear_screen()
    print_slow("АКТ III: СЕРДЦЕ ТЬМЫ")
    print_slow("\nСТОЛИЦА АРКАДИЯ")
    print_slow("\nГород окутан тьмой. В воздухе висит магия страха.")
    
    # Разные способы проникновения в зависимости от полученных предметов
    entrance_method = ""
    if game.has_artifact:
        entrance_method = "Эльфийские лучники отвлекают стражу у ворот"
    elif game.has_shadow_magic:
        entrance_method = "Телепортация с помощью магии теней"
    elif game.has_hammer:
        entrance_method = "Пролом стены в канализацию"
    elif game.has_gun_blueprint:
        entrance_method = "Взрыв ворот (начался бой)"
    elif game.has_mercenaries:
        entrance_method = "Открытый штурм с наемниками"
    elif game.has_map:
        entrance_method = "Проникновение через стоки по карте"
    else:
        entrance_method = "Скрытное проникновение с риском"
    
    print_slow(f"\nВы проникаете в город: {entrance_method}")
    
    return act5_castle()

def act5_castle():
    print_slow("\nКОРОЛЕВСКИЙ ЗАМОК")
    print_slow("\nВ замке вы встречаете капитана гвардии Одри.")
    
    # Проверка репутации для убеждения
    if game.reputation >= 2:
        print_slow('\nОдри узнает печать Ордена: "Вы принесли надежду! Я помогу вам."')
        game.convinced_captain = True
    else:
        print_slow('\nОдри смотрит с подозрением: "Я не могу доверять незнакомцу."')
        print_slow("Вам приходится действовать в одиночку.")
    
    print_slow("\nВ темнице вы находите принца - законного наследника трона.")
    
    choice = choice_prompt([
        "Освободить принца",
        "Оставить его в темнице"
    ])
    
    if choice == 1:
        game.saved_prince = True
        print_slow('\nПринц: "Спасибо! Мой отец не виновен - Морток контролирует его разум!"')
    else:
        print_slow("\nВы оставляете принца в клетке. Возможно, это ошибка...")
    
    return act6_final_showdown()

def act6_final_showdown():
    clear_screen()
    print_slow("ФИНАЛЬНАЯ БИТВА")
    print_slow("\nТРОННЫЙ ЗАЛ")
    print_slow("\nПеред вами Король, но его глаза горят зловещим зеленым светом.")
    print_slow('Голос Мортека звучит в вашей голове: "Присоединись ко мне! Вместе мы будем править вечно!"')
    
    game.mortkow_offer = True
    
    # Определяем доступные финалы на основе предыдущих выборов
    available_endings = []
    
    if game.saved_prince and game.convinced_captain:
        available_endings.append("Сразиться с Мортком и восстановить законную власть")
    
    if game.has_artifact and game.has_hammer:
        available_endings.append("Использовать артефакты для вечного заточения Мортека")
    
    available_endings.append("Пожертвовать собой, чтобы уничтожить Мортека")
    
    if game.reputation <= -2:
        available_endings.append("Принять предложение Мортека и править вместе")
    
    if not game.elf_ally and not game.dwarf_ally:
        available_endings.append("Убить всех и захватить власть самому")
    
    if game.saved_prince and game.has_mercenaries:
        available_endings.append("Убить короля и обвинить Мортека, став народным героем")
    
    print_slow("\nДоступные действия:")
    choice = choice_prompt(available_endings)
    
    ending_index = choice - 1
    selected_ending = available_endings[ending_index]
    
    return show_ending(selected_ending)

def show_ending(ending_choice):
    clear_screen()
    print_slow("ФИНАЛ")
    print_slow("\n" + "="*60)
    
    if ending_choice == "Сразиться с Мортком и восстановить законную власть":
        print_slow("ФИНАЛ 1: НОВЫЙ КОРОЛЬ")
        print_slow("\nВы побеждаете Мортека в эпической битве!")
        print_slow("Король умирает от ран, но успевает благословить сына.")
        print_slow("Принц восходит на трон, а вы становитесь Главой Ордена и Советником.")
        print_slow("Королевство вступает в новую эру мира и процветания.")
        
    elif ending_choice == "Использовать артефакты для вечного заточения Мортека":
        print_slow("ФИНАЛ 4: ВЕЧНЫЙ ПОКОЙ")
        print_slow("\nЭльфийский Рог и Гномий Молот создают печать света.")
        print_slow("Мортек не уничтожен, но заточен в вечном сне под замком.")
        print_slow("Вы становитесь Вечным Стражем, теряя человечность ради вечного мира.")
        
    elif ending_choice == "Пожертвовать собой, чтобы уничтожить Мортека":
        print_slow("ФИНАЛ 2: ЖЕРТВА ГЕРОЯ")
        print_slow("\nВы активируете древний артефакт самоуничтожения Ордена.")
        print_slow("Ослепительная вспышка стирает Мортека из реальности... и вас вместе с ним.")
        print_slow("Вы становитесь легендой, которую будут помнить тысячелетия.")
        
    elif ending_choice == "Принять предложение Мортека и править вместе":
        print_slow("ФИНАЛ 3: ВЛАСТЬ ТЬМЫ")
        print_slow("\nВы протягиваете руку Мортку. Тьма обволакивает вас.")
        print_slow("Вы становитесь Личом-вассалом, правой рукой Повелителя Тьмы.")
        print_slow("Вместе вы подчиняете королевство, устанавливая вечную тиранию.")
        
    elif ending_choice == "Убить всех и захватить власть самому":
        print_slow("ФИНАЛ 5: МАСТЕР РУИН")
        print_slow("\nВы убиваете Мортека, короля, принца - всех, кто мог претендовать на власть.")
        print_slow("Королевство погружается в хасс, а вы становитесь сильнейшим из правителей.")
        print_slow("Вы строите новую империю на обломках старой - железной рукой.")
        
    elif ending_choice == "Убить короля и обвинить Мортека, став народным героем":
        print_slow("ФИНАЛ 6: ТИРАН-ОСВОБОДИТЕЛЬ")
        print_slow("\nВы убиваете короля и сваливаете всё на Мортека.")
        print_slow("Народ провозглашает вас Освободителем и Новым Королем.")
        print_slow("Вы правите железной рукой, 'защищая' королевство от мнимых угроз.")
    
    print_slow("\n" + "="*60)
    print_slow(f"Ваша итоговая репутация: {game.reputation}")
    print_slow("Спасибо за игру в 'Хроники Павшего Королевства'!")
    
    input("\nНажмите Enter для выхода...")

# Запуск игры
if __name__ == "__main__":
    try:
        act1_start()
    except KeyboardInterrupt:
        print("\n\nИгра прервана. До свидания!")
