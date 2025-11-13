import os
import time
import json

class GameState:
    def __init__(self):
        self.current_act = "act1_start"
        self.inventory = []
        self.reputation = 0
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

    def to_dict(self):
        return {
            'current_act': self.current_act,
            'inventory': self.inventory,
            'reputation': self.reputation,
            'elf_ally': self.elf_ally,
            'dwarf_ally': self.dwarf_ally,
            'bandit_ally': self.bandit_ally,
            'has_artifact': self.has_artifact,
            'has_shadow_magic': self.has_shadow_magic,
            'has_hammer': self.has_hammer,
            'has_gun_blueprint': self.has_gun_blueprint,
            'has_mercenaries': self.has_mercenaries,
            'has_map': self.has_map,
            'saved_prince': self.saved_prince,
            'convinced_captain': self.convinced_captain,
            'mortkow_offer': self.mortkow_offer
        }

    def from_dict(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

class GameManager:
    def __init__(self):
        self.save_file = "quest_save.json"
        self.game = GameState()

    def save_game(self):
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.game.to_dict(), f, ensure_ascii=False, indent=2)
            print_slow("\n✓ Игра сохранена!")
            return True
        except Exception as e:
            print_slow(f"\n✗ Ошибка сохранения: {e}")
            return False

    def load_game(self):
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.game.from_dict(data)
                return True
            return False
        except Exception as e:
            print_slow(f"Ошибка загрузки: {e}")
            return False

    def delete_save(self):
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
                return True
        except:
            pass
        return False

    def new_game(self):
        self.game = GameState()
        return True

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def choice_prompt(options, show_save_option=True, game_manager=None):
    print("\n" + "="*50)
    
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    if show_save_option:
        print(f"{len(options) + 1}. Сохранить игру")
        print(f"{len(options) + 2}. Выйти в главное меню")
    
    while True:
        try:
            choice = int(input("\nВаш выбор: "))
            if 1 <= choice <= len(options):
                return choice
            elif show_save_option and choice == len(options) + 1:
                if game_manager:
                    game_manager.save_game()
                continue
            elif show_save_option and choice == len(options) + 2:
                return "menu"
            else:
                print("Пожалуйста, выберите существующий вариант")
        except ValueError:
            print("Введите число")

def show_status(game):
    print(f"\n--- ВАШ СТАТУС ---")
    print(f"Репутация: {game.reputation}")
    print(f"Инвентарь: {', '.join(game.inventory) if game.inventory else 'пусто'}")
    
    allies = []
    if game.elf_ally: allies.append("Эльфы")
    if game.dwarf_ally: allies.append("Гномы")
    if game.bandit_ally: allies.append("Бандиты")
    print(f"Союзники: {', '.join(allies) if allies else 'нет'}")
    
    artifacts = []
    if game.has_artifact: artifacts.append("Рог Леса")
    if game.has_shadow_magic: artifacts.append("Магия Теней")
    if game.has_hammer: artifacts.append("Рунический Молот")
    if game.has_gun_blueprint: artifacts.append("Чертеж Пушки")
    if game.has_map: artifacts.append("Тактическая Карта")
    if game.has_mercenaries: artifacts.append("Отряд Наемников")
    
    if artifacts:
        print(f"Артефакты: {', '.join(artifacts)}")

def main_menu(game_manager):
    while True:
        clear_screen()
        print_slow("ХРОНИКИ ПАВШЕГО КОРОЛЕВСТВА")
        print_slow("=" * 40)
        
        has_save = os.path.exists(game_manager.save_file)
        
        if has_save:
            print("1. Продолжить игру")
            print("2. Новая игра")
            print("3. Удалить сохранение")
            print("4. Выйти")
        else:
            print("1. Новая игра")
            print("2. Выйти")
        
        try:
            choice = int(input("\nВаш выбор: "))
            
            if has_save:
                if choice == 1:
                    if game_manager.load_game():
                        print_slow("Загрузка сохранения...")
                        time.sleep(1)
                        return True
                    else:
                        print_slow("Ошибка загрузки сохранения!")
                        time.sleep(2)
                elif choice == 2:
                    if new_game_confirmation(game_manager):
                        return True
                elif choice == 3:
                    if game_manager.delete_save():
                        print_slow("Сохранение удалено!")
                    else:
                        print_slow("Не удалось удалить сохранение!")
                    time.sleep(2)
                elif choice == 4:
                    return False
            else:
                if choice == 1:
                    if new_game_confirmation(game_manager):
                        return True
                elif choice == 2:
                    return False
                    
        except ValueError:
            print("Пожалуйста, введите число")
            time.sleep(1)

def new_game_confirmation(game_manager):
    if os.path.exists(game_manager.save_file):
        print("\nУ вас есть незавершенная игра. Начать новую?")
        print("1. Да, удалить текущее сохранение")
        print("2. Нет, вернуться в меню")
        
        try:
            choice = int(input("Ваш выбор: "))
            if choice == 1:
                game_manager.delete_save()
                game_manager.new_game()
                return True
            return False
        except ValueError:
            return False
    else:
        game_manager.new_game()
        return True

# Игровые акты
def act1_start(game_manager):
    game_manager.game.current_act = "act1_start"
    game_manager.save_game()
    
    clear_screen()
    print_slow("АКТ I: ПРОБУЖДЕНИЕ")
    print_slow("\nВы приходите в сознание среди дымящихся руин цитадели Ордена Серебряного Феникса.")
    print_slow("Ваш Магистр, истекая кровью, протягивает вам печать Ордена.")
    print_slow('"Морток... король... предан... Ищи ответы..."')
    print_slow('"Лес... Шахты... Равнины..."')
    show_status(game_manager.game)
    print_slow("\nПеред вами три пути:")
    
    choice = choice_prompt([
        "Отправиться в Таинственный Лес Эльфов",
        "Спуститься в Заброшенные Шахты Гномов", 
        "Исследовать Выжженные Равнины"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        return act2_elf_forest(game_manager)
    elif choice == 2:
        return act2_dwarf_mines(game_manager)
    else:
        return act2_burned_plains(game_manager)

def act2_elf_forest(game_manager):
    game_manager.game.current_act = "act2_elf_forest"
    game_manager.save_game()
    
    clear_screen()
    print_slow("ЛЕС ЭЛЬФОВ")
    print_slow("\nВы входите в древний лес. Воздух звенит магией.")
    print_slow("Эльфийский дозорный появляется из-за деревьев.")
    print_slow('"Человек! Что привело тебя в наши владения?"')
    show_status(game_manager.game)
    
    choice = choice_prompt([
        "Показать печать Ордена и попросить помощи",
        "Попытаться пробраться тайком вглубь леса"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        print_slow('\n"Печать Серебряного Феникса... Я помню этот орден."')
        print_slow('"Но доверия нужно заслужить. Наше Лесное Сердце отравлено скверной Мортека."')
        return act3_elf_quest(game_manager)
    else:
        print_slow("\nВы пытаетесь обойти дозорных, но эльфийская магия обнаруживает вас.")
        print_slow("Вас захватывают и ведут к Королеве Эльфов.")
        return act3_elf_betrayal(game_manager)

def act3_elf_quest(game_manager):
    game_manager.game.current_act = "act3_elf_quest"
    game_manager.save_game()
    
    print_slow("\nКоролева Эльфов взирает на вас с подозрением.")
    print_slow('"Очисти Лесное Сердце от скверны, и мы поможем тебе."')
    show_status(game_manager.game)
    
    print_slow("\nВы находите источник порчи - кристалл тьмы, питающийся магией леса.")
    
    choice = choice_prompt([
        "Провести ритуал очищения (собрать три священные травы)",
        "Разрушить кристалл силой оружия"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        print_slow("\nВы собираете Лунный Цветок, Звездную Пыль и Слезу Феникса.")
        print_slow("Ритуал очищения проходит успешно! Лес наполняется светом.")
        print_slow('Королева дарует вам РОГ ЛЕСА - артефакт, призывающий эльфийских лучников.')
        game_manager.game.elf_ally = True
        game_manager.game.has_artifact = True
        game_manager.game.reputation += 2
        game_manager.game.inventory.append("Рог Леса")
    else:
        print_slow("\nВы атакуете кристалл, но обратная волна магии ранит вас.")
        print_slow("Эльфы спасают вас, но доверия не прибавляется.")
        game_manager.game.reputation += 1
    
    game_manager.save_game()
    return act4_capital(game_manager)

def act3_elf_betrayal(game_manager):
    game_manager.game.current_act = "act3_elf_betrayal"
    game_manager.save_game()
    
    print_slow('\n"Вор и шпион! Ты заплатишь за это!"')
    
    choice = choice_prompt([
        "Попытаться договориться",
        "Сражаться до конца",
        "Украсть эльфийскую реликвию и бежать"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        print_slow("\nВам удается убедить эльфов в своих добрых намерениях.")
        print_slow("Они отпускают вас, но помощи не предлагают.")
        game_manager.game.reputation -= 1
    elif choice == 2:
        print_slow("\nВы сражаетесь отчаянно, но против магии эльфов нет шансов.")
        print_slow("Вас изгоняют из леса.")
        game_manager.game.reputation -= 2
    else:
        print_slow("\nПока эльфы спорят о вашей судьбе, вы крадете СФЕРУ ТЕНЕЙ.")
        print_slow("Древний артефакт дает вам доступ к запретной магии.")
        game_manager.game.has_shadow_magic = True
        game_manager.game.reputation -= 3
        game_manager.game.inventory.append("Сфера Теней")
    
    game_manager.save_game()
    return act4_capital(game_manager)

def act2_dwarf_mines(game_manager):
    game_manager.game.current_act = "act2_dwarf_mines"
    game_manager.save_game()
    
    clear_screen()
    print_slow("ШАХТЫ ГНОМОВ")
    print_slow("\nГорный проход завален камнями. Слышны крики и лязг оружия изнутри.")
    
    choice = choice_prompt([
        "Разобрать завал и помочь гномам",
        "Найти обходной путь через вентиляционные шахты"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        print_slow("\nВы пробиваетесь внутрь и видите гномов, сражающихся с троллями.")
        return act3_dwarf_battle(game_manager)
    else:
        print_slow("\nОбходной путь ведет в заброшенную мастерскую.")
        return act3_dwarf_workshop(game_manager)

def act3_dwarf_battle(game_manager):
    game_manager.game.current_act = "act3_dwarf_battle"
    game_manager.save_game()
    
    print_slow("\nКороль Гномов кричит: 'Помоги нам, человек, и мы не забудем эту услугу!'")
    
    choice = choice_prompt([
        "Атаковать троллей вместе с гномами",
        "Починить древнюю откачивающую помпу и затопить пещеры троллей"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        print_slow("\nВместе вы побеждаете троллей! Гномы ликуют.")
        print_slow('К
    
    if choice == 1:
        print_slow("\nГномы восхищены вашей честностью.")
        print_slow("В награду они делятся с вами секретами рунической магии.")
        game_manager.game.dwarf_ally = True
        game_manager.game.reputation += 2
    else:
        print_slow("\nВы крадете чертеж и скрываетесь. Теперь у вас есть мощное оружие.")
        print_slow("Но гномы поклялись отомстить.")
        game_manager.game.has_gun_blueprint = True
        game_manager.game.reputation -= 2
        game_manager.game.inventory.append("Чертеж Огненной Пушки")
    
    game_manager.save_game()
    return act4_capital(game_manager)

def act2_burned_plains(game_manager):
    game_manager.game.current_act = "act2_burned_plains"
    game_manager.save_game()
    
    clear_screen()
    print_slow("ВЫЖЖЕННЫЕ РАВНИНЫ")
    print_slow("\nБескрайние пустоши, где выживают только сильнейшие.")
    print_slow("Вы находите лагерь банды 'Вольные Соколы'.")
    
    choice = choice_prompt([
        "Предложить свои услуги бандитам",
        "Напасть на бандитов и забрать их припасы",
        "Обойти лагерь и искать другие пути"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        return act3_bandit_join(game_manager)
    elif choice == 2:
        return act3_bandit_fight(game_manager)
    else:
        return act3_bandit_stealth(game_manager)

def act3_bandit_join(game_manager):
    game_manager.game.current_act = "act3_bandit_join"
    game_manager.save_game()
    
    print_slow("\nЛидер банды Гаррет оценивающе смотрит на вас.")
    print_slow('"Хочешь присоединиться? Докажи преданность - ограбь королевский караван."')
    
    choice = choice_prompt([
        "Согласиться и участвовать в ограблении",
        "Отказаться и уйти"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        print_slow("\nОграбление проходит успешно! Гаррет доволен.")
        print_slow("Теперь у вас есть ОТРЯД НАЕМНИКОВ для штурма замка.")
        game_manager.game.bandit_ally = True
        game_manager.game.has_mercenaries = True
        game_manager.game.reputation -= 2
        game_manager.game.inventory.append("Отряд Наемников")
    else:
        print_slow("\nГаррет смеется: 'Мягкотелый рыцарь!' Но отпускает вас.")
        game_manager.game.reputation += 1
    
    game_manager.save_game()
    return act4_capital(game_manager)

def act3_bandit_fight(game_manager):
    game_manager.game.current_act = "act3_bandit_fight"
    game_manager.save_game()
    
    print_slow("\nВы нападаете на бандитов. Завязалась жестокая схватка!")
    
    if game_manager.game.has_hammer or game_manager.game.has_shadow_magic:
        print_slow("Ваше оружие/магия дают преимущество! Вы побеждаете.")
        print_slow("Среди вещей Гаррета вы находите ТАКТИЧЕСКУЮ КАРТУ патрулей.")
        game_manager.game.has_map = True
        game_manager.game.inventory.append("Тактическая Карта")
        game_manager.game.reputation += 1
    else:
        print_slow("Бандитов слишком много! Вам едва удается спастись.")
        game_manager.game.reputation += 1
    
    game_manager.save_game()
    return act4_capital(game_manager)

def act3_bandit_stealth(game_manager):
    game_manager.game.current_act = "act3_bandit_stealth"
    game_manager.save_game()
    
    print_slow("\nВы обходите лагерь и находите заброшенный наблюдательный пост.")
    print_slow("Среди бумаг - карты и документы о передвижениях войск Мортека.")
    
    game_manager.game.has_map = True
    game_manager.game.inventory.append("Тактическая Карта")
    game_manager.game.reputation += 1
    game_manager.save_game()
    return act4_capital(game_manager)

def act4_capital(game_manager):
    game_manager.game.current_act = "act4_capital"
    game_manager.save_game()
    
    clear_screen()
    print_slow("АКТ III: СЕРДЦЕ ТЬМЫ")
    print_slow("\nСТОЛИЦА АРКАДИЯ")
    print_slow("\nГород окутан тьмой. В воздухе висит магия страха.")
    show_status(game_manager.game)
    
    entrance_method = ""
    if game_manager.game.has_artifact:
        entrance_method = "Эльфийские лучники отвлекают стражу у ворот"
    elif game_manager.game.has_shadow_magic:
        entrance_method = "Телепортация с помощью магии теней"
    elif game_manager.game.has_hammer:
        entrance_method = "Пролом стены в канализацию"
    elif game_manager.game.has_gun_blueprint:
        entrance_method = "Взрыв ворот (начался бой)"
    elif game_manager.game.has_mercenaries:
        entrance_method = "Открытый штурм с наемниками"
    elif game_manager.game.has_map:
        entrance_method = "Проникновение через стоки по карте"
    else:
        entrance_method = "Скрытное проникновение с риском"
    
    print_slow(f"\nВы проникаете в город: {entrance_method}")
    
    return act5_castle(game_manager)

def act5_castle(game_manager):
    game_manager.game.current_act = "act5_castle"
    game_manager.save_game()
    
    print_slow("\nКОРОЛЕВСКИЙ ЗАМОК")
    print_slow("\nВ замке вы встречаете капитана гвардии Одри.")
    show_status(game_manager.game)
    
    if game_manager.game.reputation >= 2:
        print_slow('\nОдри узнает печать Ордена: "Вы принесли надежду! Я помогу вам."')
        game_manager.game.convinced_captain = True
    else:
        print_slow('\nОдри смотрит с подозрением: "Я не могу доверять незнакомцу."')
        print_slow("Вам приходится действовать в одиночку.")
    
    print_slow("\nВ темнице вы находите принца - законного наследника трона.")
    
    choice = choice_prompt([
        "Освободить принца",
        "Оставить его в темнице"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        game_manager.game.saved_prince = True
        print_slow('\nПринц: "Спасибо! Мой отец не виновен - Морток контролирует его разум!"')
    else:
        print_slow("\nВы оставляете принца в клетке. Возможно, это ошибка...")
    
    game_manager.save_game()
    return act6_final_showdown(game_manager)

def act6_final_showdown(game_manager):
    game_manager.game.current_act = "act6_final_showdown"
    game_manager.save_game()
    
    clear_screen()
    print_slow("ФИНАЛЬНАЯ БИТВА")
    print_slow("\nТРОННЫЙ ЗАЛ")
    print_slow("\nПеред вами Король, но его глаза горят зловещим зеленым светом.")
    print_slow('Голос Мортека звучит в вашей голове: "Присоединись ко мне! Вместе мы будем править вечно!"')
    show_status(game_manager.game)
    
    game_manager.game.mortkow_offer = True
    
    available_endings = []
    
    if game_manager.game.saved_prince and game_manager.game.convinced_captain:
        available_endings.append("Сразиться с Мортком и восстановить законную власть")
    
    if game_manager.game.has_artifact and game_manager.game.has_hammer:
        available_endings.append("Использовать артефакты для вечного заточения Мортека")
    
    available_endings.append("Пожертвовать собой, чтобы уничтожить Мортека")
    
    if game_manager.game.reputation <= -2:
        available_endings.append("Принять предложение Мортека и править вместе")
    
    if not game_manager.game.elf_ally and not game_manager.game.dwarf_ally:
        available_endings.append("Убить всех и захватить власть самому")
    
    if game_manager.game.saved_prince and game_manager.game.has_mercenaries:
        available_endings.append("Убить короля и обвинить Мортека, став народным героем")
    
    print_slow("\nДоступные действия:")
    choice = choice_prompt(available_endings, show_save_option=False, game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    ending_index = choice - 1
    selected_ending = available_endings[ending_index]
    
    game_manager.delete_save()
    return show_ending(selected_ending, game_manager.game)

def show_ending(ending_choice, game):
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
    
    input("\nНажмите Enter для возврата в главное меню...")
    return "menu"

def start_game_loop(game_manager):
    act_functions = {
        "act1_start": act1_start,
        "act2_elf_forest": act2_elf_forest,
        "act3_elf_quest": act3_elf_quest,
        "act3_elf_betrayal": act3_elf_betrayal,
        "act2_dwarf_mines": act2_dwarf_mines,
        "act3_dwarf_battle": act3_dwarf_battle,
        "act3_dwarf_workshop": act3_dwarf_workshop,
        "act2_burned_plains": act2_burned_plains,
        "act3_bandit_join": act3_bandit_join,
        "act3_bandit_fight": act3_bandit_fight,
        "act3_bandit_stealth": act3_bandit_stealth,
        "act4_capital": act4_capital,
        "act5_castle": act5_castle,
        "act6_final_showdown": act6_final_showdown,
    }
    
    current_act = game_manager.game.current_act
    if current_act in act_functions:
        return act_functions[current_act](game_manager)
    else:
        return act1_start(game_manager)

def main():
    game_manager = GameManager()
    
    try:
        while True:
            if not main_menu(game_manager):
                break
                
            result = start_game_loop(game_manager)
            
            if result == "menu":
                continue
                
    except KeyboardInterrupt:
        print("\n\nИгра прервана. До свидания!")
    except Exception as e:
        print(f"\n\nПроизошла ошибка: {e}")
        print("Попробуйте запустить игру снова.")

if __name__ == "__main__":
    main()ороль дарует вам ДРЕВНИЙ РУНИЧЕСКИЙ МОЛОТ.')
        game_manager.game.dwarf_ally = True
        game_manager.game.has_hammer = True
        game_manager.game.reputation += 2
        game_manager.game.inventory.append("Рунический Молот")
    else:
        print_slow("\nВы находите механизм и запускаете его. Тролли тонут в подземных водах.")
        print_slow("Гномы благодарны, но некоторые сомневаются в ваших методах.")
        game_manager.game.reputation += 1
    
    game_manager.save_game()
    return act4_capital(game_manager)

def act3_dwarf_workshop(game_manager):
    game_manager.game.current_act = "act3_dwarf_workshop"
    game_manager.save_game()
    
    print_slow("\nВ мастерской вы находите чертежи древнего оружия.")
    
    choice = choice_prompt([
        "Вернуть чертежи гномам",
        "Украсть чертеж ОГНЕННОЙ ПУШКИ и уйти незамеченным"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        print_slow("\nГномы восхищены вашей честностью.")
        print_slow("В награду они делятся с вами секретами рунической магии.")
        game_manager.game.dwarf_ally = True
        game_manager.game.reputation += 2
    else:
        print_slow("\nВы крадете чертеж и скрываетесь. Теперь у вас есть мощное оружие.")
        print_slow("Но гномы поклялись отомстить.")
        game_manager.game.has_gun_blueprint = True
        game_manager.game.reputation -= 2
        game_manager.game.inventory.append("Чертеж Огненной Пушки")
    
    game_manager.save_game()
    return act4_capital(game_manager)

def act2_burned_plains(game_manager):
    game_manager.game.current_act = "act2_burned_plains"
    game_manager.save_game()
    
    clear_screen()
    print_slow("ВЫЖЖЕННЫЕ РАВНИНЫ")
    print_slow("\nБескрайние пустоши, где выживают только сильнейшие.")
    print_slow("Вы находите лагерь банды 'Вольные Соколы'.")
    
    choice = choice_prompt([
        "Предложить свои услуги бандитам",
        "Напасть на бандитов и забрать их припасы",
        "Обойти лагерь и искать другие пути"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        return act3_bandit_join(game_manager)
    elif choice == 2:
        return act3_bandit_fight(game_manager)
    else:
        return act3_bandit_stealth(game_manager)

def act3_bandit_join(game_manager):
    game_manager.game.current_act = "act3_bandit_join"
    game_manager.save_game()
    
    print_slow("\nЛидер банды Гаррет оценивающе смотрит на вас.")
    print_slow('"Хочешь присоединиться? Докажи преданность - ограбь королевский караван."')
    
    choice = choice_prompt([
        "Согласиться и участвовать в ограблении",
        "Отказаться и уйти"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        print_slow("\nОграбление проходит успешно! Гаррет доволен.")
        print_slow("Теперь у вас есть ОТРЯД НАЕМНИКОВ для штурма замка.")
        game_manager.game.bandit_ally = True
        game_manager.game.has_mercenaries = True
        game_manager.game.reputation -= 2
        game_manager.game.inventory.append("Отряд Наемников")
    else:
        print_slow("\nГаррет смеется: 'Мягкотелый рыцарь!' Но отпускает вас.")
        game_manager.game.reputation += 1
    
    game_manager.save_game()
    return act4_capital(game_manager)

def act3_bandit_fight(game_manager):
    game_manager.game.current_act = "act3_bandit_fight"
    game_manager.save_game()
    
    print_slow("\nВы нападаете на бандитов. Завязалась жестокая схватка!")
    
    if game_manager.game.has_hammer or game_manager.game.has_shadow_magic:
        print_slow("Ваше оружие/магия дают преимущество! Вы побеждаете.")
        print_slow("Среди вещей Гаррета вы находите ТАКТИЧЕСКУЮ КАРТУ патрулей.")
        game_manager.game.has_map = True
        game_manager.game.inventory.append("Тактическая Карта")
        game_manager.game.reputation += 1
    else:
        print_slow("Бандитов слишком много! Вам едва удается спастись.")
        game_manager.game.reputation += 1
    
    game_manager.save_game()
    return act4_capital(game_manager)

def act3_bandit_stealth(game_manager):
    game_manager.game.current_act = "act3_bandit_stealth"
    game_manager.save_game()
    
    print_slow("\nВы обходите лагерь и находите заброшенный наблюдательный пост.")
    print_slow("Среди бумаг - карты и документы о передвижениях войск Мортека.")
    
    game_manager.game.has_map = True
    game_manager.game.inventory.append("Тактическая Карта")
    game_manager.game.reputation += 1
    game_manager.save_game()
    return act4_capital(game_manager)

def act4_capital(game_manager):
    game_manager.game.current_act = "act4_capital"
    game_manager.save_game()
    
    clear_screen()
    print_slow("АКТ III: СЕРДЦЕ ТЬМЫ")
    print_slow("\nСТОЛИЦА АРКАДИЯ")
    print_slow("\nГород окутан тьмой. В воздухе висит магия страха.")
    show_status(game_manager.game)
    
    entrance_method = ""
    if game_manager.game.has_artifact:
        entrance_method = "Эльфийские лучники отвлекают стражу у ворот"
    elif game_manager.game.has_shadow_magic:
        entrance_method = "Телепортация с помощью магии теней"
    elif game_manager.game.has_hammer:
        entrance_method = "Пролом стены в канализацию"
    elif game_manager.game.has_gun_blueprint:
        entrance_method = "Взрыв ворот (начался бой)"
    elif game_manager.game.has_mercenaries:
        entrance_method = "Открытый штурм с наемниками"
    elif game_manager.game.has_map:
        entrance_method = "Проникновение через стоки по карте"
    else:
        entrance_method = "Скрытное проникновение с риском"
    
    print_slow(f"\nВы проникаете в город: {entrance_method}")
    
    return act5_castle(game_manager)

def act5_castle(game_manager):
    game_manager.game.current_act = "act5_castle"
    game_manager.save_game()
    
    print_slow("\nКОРОЛЕВСКИЙ ЗАМОК")
    print_slow("\nВ замке вы встречаете капитана гвардии Одри.")
    show_status(game_manager.game)
    
    if game_manager.game.reputation >= 2:
        print_slow('\nОдри узнает печать Ордена: "Вы принесли надежду! Я помогу вам."')
        game_manager.game.convinced_captain = True
    else:
        print_slow('\nОдри смотрит с подозрением: "Я не могу доверять незнакомцу."')
        print_slow("Вам приходится действовать в одиночку.")
    
    print_slow("\nВ темнице вы находите принца - законного наследника трона.")
    
    choice = choice_prompt([
        "Освободить принца",
        "Оставить его в темнице"
    ], game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    if choice == 1:
        game_manager.game.saved_prince = True
        print_slow('\nПринц: "Спасибо! Мой отец не виновен - Морток контролирует его разум!"')
    else:
        print_slow("\nВы оставляете принца в клетке. Возможно, это ошибка...")
    
    game_manager.save_game()
    return act6_final_showdown(game_manager)

def act6_final_showdown(game_manager):
    game_manager.game.current_act = "act6_final_showdown"
    game_manager.save_game()
    
    clear_screen()
    print_slow("ФИНАЛЬНАЯ БИТВА")
    print_slow("\nТРОННЫЙ ЗАЛ")
    print_slow("\nПеред вами Король, но его глаза горят зловещим зеленым светом.")
    print_slow('Голос Мортека звучит в вашей голове: "Присоединись ко мне! Вместе мы будем править вечно!"')
    show_status(game_manager.game)
    
    game_manager.game.mortkow_offer = True
    
    available_endings = []
    
    if game_manager.game.saved_prince and game_manager.game.convinced_captain:
        available_endings.append("Сразиться с Мортком и восстановить законную власть")
    
    if game_manager.game.has_artifact and game_manager.game.has_hammer:
        available_endings.append("Использовать артефакты для вечного заточения Мортека")
    
    available_endings.append("Пожертвовать собой, чтобы уничтожить Мортека")
    
    if game_manager.game.reputation <= -2:
        available_endings.append("Принять предложение Мортека и править вместе")
    
    if not game_manager.game.elf_ally and not game_manager.game.dwarf_ally:
        available_endings.append("Убить всех и захватить власть самому")
    
    if game_manager.game.saved_prince and game_manager.game.has_mercenaries:
        available_endings.append("Убить короля и обвинить Мортека, став народным героем")
    
    print_slow("\nДоступные действия:")
    choice = choice_prompt(available_endings, show_save_option=False, game_manager=game_manager)
    
    if choice == "menu":
        return "menu"
    
    ending_index = choice - 1
    selected_ending = available_endings[ending_index]
    
    game_manager.delete_save()
    return show_ending(selected_ending, game_manager.game)

def show_ending(ending_choice, game):
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
    
    input("\nНажмите Enter для возврата в главное меню...")
    return "menu"

def start_game_loop(game_manager):
    act_functions = {
        "act1_start": act1_start,
        "act2_elf_forest": act2_elf_forest,
        "act3_elf_quest": act3_elf_quest,
        "act3_elf_betrayal": act3_elf_betrayal,
        "act2_dwarf_mines": act2_dwarf_mines,
        "act3_dwarf_battle": act3_dwarf_battle,
        "act3_dwarf_workshop": act3_dwarf_workshop,
        "act2_burned_plains": act2_burned_plains,
        "act3_bandit_join": act3_bandit_join,
        "act3_bandit_fight": act3_bandit_fight,
        "act3_bandit_stealth": act3_bandit_stealth,
        "act4_capital": act4_capital,
        "act5_castle": act5_castle,
        "act6_final_showdown": act6_final_showdown,
    }
    
    current_act = game_manager.game.current_act
    if current_act in act_functions:
        return act_functions[current_act](game_manager)
    else:
        return act1_start(game_manager)

def main():
    game_manager = GameManager()
    
    try:
        while True:
            if not main_menu(game_manager):
                break
                
            result = start_game_loop(game_manager)
            
            if result == "menu":
                continue
                
    except KeyboardInterrupt:
        print("\n\nИгра прервана. До свидания!")
    except Exception as e:
        print(f"\n\nПроизошла ошибка: {e}")
        print("Попробуйте запустить игру снова.")

if __name__ == "__main__":
    main()
