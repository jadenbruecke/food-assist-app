import initializer
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
from PyQt5 import uic
import res_rc
import sys
import steps.step_1_ui as step1Ui
import steps.step_2_ui as step2Ui
import steps.step_3_ui as step3Ui
import steps.step_4_ui as step4Ui
import result_step_page_ui as resUi

class FoodAssist(qtw.QWidget):
  def __init__(self, my_initializer):
    super().__init__()
    self.ui = uic.loadUi('ui/xx_xx_start.ui', self)

    # pass on my_initializer
    self.my_initializer = my_initializer
    self.my_initializer.current_step = None
    self.my_initializer.devices_connected.connect(self.onMobileConnected)
    self.my_initializer.devices_disconnected.connect(self.onMobileDisconnected)

    # set icons upon loading
    if self.my_initializer.devices_running:
      self.status_phone.setPixmap(qtg.QPixmap('ui/resources/Phone On.svg'))
      self.status_watch.setPixmap(qtg.QPixmap('ui/resources/Watch On.svg'))
    else:
      self.status_phone.setPixmap(qtg.QPixmap('ui/resources/Phone Off.svg'))
      self.status_watch.setPixmap(qtg.QPixmap('ui/resources/Watch Off.svg'))

    self.start_button.clicked.connect(self.button_pressed)
    # draw finger-tip cursor
    draw_finger_tip_cursor(self)
    # Hand tracking thread
    self.my_initializer.hand_position.connect(self.onHandPositionArrival)
    self.my_initializer.obj.reset_counter()

  def paintEvent(self, event):
    self.cursor_widget.move(self.finger_tip_x, self.finger_tip_y)

  # check if the button is touched
  def onHandPositionArrival(self, x, y, z, counter, cursor_x, cursor_y):
    # draw cursor for finger tip
    self.finger_tip_x = cursor_x
    self.finger_tip_y = cursor_y
    # UI update calling paintEvent()
    self.update()
    # check whether hand position is in area
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.large) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.start_button.click()

  @qtc.pyqtSlot()
  def button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = Language_and_Hand_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

  # check if phone and watch are connected
  def onMobileConnected(self):
    self.status_phone.setPixmap(qtg.QPixmap('ui/resources/Phone On.svg'))
    self.status_watch.setPixmap(qtg.QPixmap('ui/resources/Watch On.svg'))

  # check if phone and watch are connected
  def onMobileDisconnected(self):
    self.status_phone.setPixmap(qtg.QPixmap('ui/resources/Phone Off.svg'))
    self.status_watch.setPixmap(qtg.QPixmap('ui/resources/Watch Off.svg'))

class Language_and_Hand_UI(qtw.QWidget):
  def __init__(self, my_initializer):
    super().__init__()
    self.ui = uic.loadUi('ui/xx_xx_settings.ui', self)
    # pass on my_initializer
    self.my_initializer = my_initializer
    self.my_initializer.current_step = None

    self.lang = None
    self.hand = None

    self.button_yes.setHidden(True)
    self.button_yes.setEnabled(False)
    self.button_no.setHidden(True)
    self.button_no.setEnabled(False)
    self.button_heading.setHidden(True)
    self.button_heading.setEnabled(False)

    self.button_de.clicked.connect(lambda: self.choose_lang('de'))
    self.button_en.clicked.connect(lambda: self.choose_lang('en'))
    self.button_left_shoulder.clicked.connect(lambda: self.choose_hand('left'))
    self.button_right_shoulder.clicked.connect(lambda: self.choose_hand('right'))
    self.button_yes.clicked.connect(self.yes_button_pressed)
    self.button_no.clicked.connect(self.no_button_pressed)

    # draw finger-tip cursor
    draw_finger_tip_cursor(self)
    # Hand tracking thread
    self.my_initializer.hand_position.connect(self.onHandPositionArrival)
    self.my_initializer.obj.reset_counter()

  def paintEvent(self, event):
    self.cursor_widget.move(self.finger_tip_x, self.finger_tip_y)
    if self.lang and self.hand:
      self.button_yes.setHidden(False)
      self.button_yes.setEnabled(True)
      self.button_no.setHidden(False)
      self.button_no.setEnabled(True)
      self.button_heading.setHidden(False)
      self.button_heading.setEnabled(True)

  # check if the button is touched
  def onHandPositionArrival(self, x, y, z, counter, cursor_x, cursor_y):
    # draw cursor for finger tip
    self.finger_tip_x = cursor_x
    self.finger_tip_y = cursor_y
    self.update()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_a) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_yes.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_b) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_no.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_de) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_de.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_en) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_en.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_left_shoulder) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_left_shoulder.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_right_shoulder) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_right_shoulder.click()

  @qtc.pyqtSlot()
  def choose_lang(self, lang):
    change_active_button_color(self, lang)
    self.lang = lang
  
  @qtc.pyqtSlot()
  def choose_hand(self, hand):
    change_active_button_color(self, hand)
    self.hand = hand
  
  @qtc.pyqtSlot()
  def yes_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.my_initializer.lang = self.lang
    self.my_initializer.hand = self.hand
    self.target_ui = Placing_Meat_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()
  
  @qtc.pyqtSlot()
  def no_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.lang = None
    self.hand = None
    self.target_ui = FoodAssist(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

class Placing_Meat_UI(qtw.QWidget):
  def __init__(self, my_initializer):
    super().__init__()
    self.ui = uic.loadUi('ui/xx_xx_placing_meat.ui', self)
    # pass on my_initializer
    self.my_initializer = my_initializer
    self.my_initializer.current_step = None
    self.my_initializer.detection_params.connect(self.draw_detection_box)

    self.box_x = 0
    self.box_y = 0
    self.box_w = 0
    self.box_h = 0

    self.button_skip.clicked.connect(self.skip_step_detection)
    self.detection_gif = qtg.QMovie('ui/resources/Detecting Icon.gif')
    self.detecting_gif_label.setMovie(self.detection_gif)
    self.detection_gif.start()
    self.step_consistency_counter = 0

    # draw finger-tip cursor
    draw_finger_tip_cursor(self)
    # Hand tracking thread
    self.my_initializer.hand_position.connect(self.onHandPositionArrival)
    self.my_initializer.obj.reset_counter()

  # paints detection box on UI based on parameter (x,y,w,h) and triggered by event (self.update())
  def paintEvent(self, event):
    print("In Paint event (x,y,w.h): ", self.box_x, self.box_y, self.box_w, self.box_h )
    box_painter = qtg.QPainter(self)
    box_painter.setRenderHint(qtg.QPainter.Antialiasing)
    path = qtg.QPainterPath()
    path.addRoundedRect(qtc.QRectF(self.box_x, self.box_y, self.box_w, self.box_h), 5, 5)
    pen = qtg.QPen(qtc.Qt.GlobalColor.yellow, 5)
    box_painter.setPen(pen)
    box_painter.fillPath(path, qtc.Qt.GlobalColor.transparent)
    box_painter.drawPath(path)
    self.cursor_widget.move(self.finger_tip_x, self.finger_tip_y)
    # navigate when 5 consistent detection has occured
    if self.step_consistency_counter == 5:
      self.navigate_to_detected_step()

  # check if the button is touched
  def onHandPositionArrival(self, x, y, z, counter, cursor_x, cursor_y):
    # draw cursor for finger tip
    self.finger_tip_x = cursor_x
    self.finger_tip_y = cursor_y
    self.update()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.large) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_skip.click()

  @qtc.pyqtSlot()
  def skip_step_detection(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = Entry_Step_1_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()
  
  @qtc.pyqtSlot()
  def navigate_to_detected_step(self):
    if self.my_initializer.detected_step == 1:
      self.my_initializer.hand_position.disconnect()
      self.target_ui = Entry_Step_1_UI(self.my_initializer)
      select_screen_and_show(self.target_ui)
      self.close()

  def draw_detection_box(self, x, y, width, height, step):
    print('Detection box parameters from model: (x, y, w, h)', x, y, width, height)
    print('Detected step: ', step)
    self.box_x = x
    self.box_y = y
    self.box_w = width
    self.box_h = height
    self.update()
    if step != 0:
      self.step_consistency_counter += 1
    else:
      self.step_consistency_counter = 0

class Entry_Step_1_UI(qtw.QWidget):
  def __init__(self, my_initializer):
    super().__init__()
    # pass on my_initializer
    self.my_initializer = my_initializer
    self.my_initializer.current_step = None

    self.ui = uic.loadUi(f'ui/{my_initializer.lang}_{my_initializer.hand}_entry_step1.ui', self)
    self.button_yes.clicked.connect(self.yes_button_pressed)
    self.button_no.clicked.connect(self.no_button_pressed)

    # draw finger-tip cursor
    draw_finger_tip_cursor(self)
    # Hand tracking thread
    self.my_initializer.hand_position.connect(self.onHandPositionArrival)
    self.my_initializer.obj.reset_counter()

  def paintEvent(self, event):
    self.cursor_widget.move(self.finger_tip_x, self.finger_tip_y)
  
  # check if the button is touched
  def onHandPositionArrival(self, x, y, z, counter, cursor_x, cursor_y):
    # draw cursor for finger tip
    self.finger_tip_x = cursor_x
    self.finger_tip_y = cursor_y
    self.update()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_a) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_yes.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_b) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_no.click()

  @qtc.pyqtSlot()
  def yes_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = step1Ui.Step_1_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

  @qtc.pyqtSlot()
  def no_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.my_initializer.last_class = Entry_Step_1_UI
    self.target_ui = Menu_Default_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

class Entry_Step_2_UI(qtw.QWidget):
  def __init__(self, my_initializer):
    super().__init__()
    # pass on my_initializer
    self.my_initializer = my_initializer
    self.my_initializer.current_step = None
    self.ui = uic.loadUi(f'ui/{my_initializer.lang}_{my_initializer.hand}_entry_step2.ui', self)
    self.button_yes.clicked.connect(self.yes_button_pressed)
    self.button_no.clicked.connect(self.no_button_pressed)

    # draw finger-tip cursor
    draw_finger_tip_cursor(self)
    # Hand tracking thread
    self.my_initializer.hand_position.connect(self.onHandPositionArrival)
    self.my_initializer.obj.reset_counter()

  def paintEvent(self, event):
    self.cursor_widget.move(self.finger_tip_x, self.finger_tip_y)
  
  # check if the button is touched
  def onHandPositionArrival(self, x, y, z, counter, cursor_x, cursor_y):
    # draw cursor for finger tip
    self.finger_tip_x = cursor_x
    self.finger_tip_y = cursor_y
    self.update()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_a) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_yes.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_b) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_no.click()

  @qtc.pyqtSlot()
  def yes_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = step2Ui.Step_2_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

  @qtc.pyqtSlot()
  def no_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.my_initializer.last_class = Entry_Step_2_UI
    self.target_ui = Menu_Default_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

class Entry_Step_3_UI(qtw.QWidget):
  def __init__(self, my_initializer):
    super().__init__()
    # pass on my_initializer
    self.my_initializer = my_initializer
    self.my_initializer.current_step = None

    self.ui = uic.loadUi(f'ui/{my_initializer.lang}_{my_initializer.hand}_entry_step3.ui', self)
    self.button_yes.clicked.connect(self.yes_button_pressed)
    self.button_no.clicked.connect(self.no_button_pressed)

    # draw finger-tip cursor
    draw_finger_tip_cursor(self)
    # Hand tracking thread
    self.my_initializer.hand_position.connect(self.onHandPositionArrival)
    self.my_initializer.obj.reset_counter()
  
  def paintEvent(self, event):
    self.cursor_widget.move(self.finger_tip_x, self.finger_tip_y)
  
  # check if the button is touched
  def onHandPositionArrival(self, x, y, z, counter, cursor_x, cursor_y):
    # draw cursor for finger tip
    self.finger_tip_x = cursor_x
    self.finger_tip_y = cursor_y
    self.update()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_a) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_yes.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_b) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_no.click()
  
  @qtc.pyqtSlot()
  def yes_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = step3Ui.Step_3_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

  @qtc.pyqtSlot()
  def no_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.my_initializer.last_class = Entry_Step_3_UI
    self.target_ui = Menu_Default_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

class Entry_Step_4_UI(qtw.QWidget):
  def __init__(self, my_initializer):
    super().__init__()
    # pass on my_initializer
    self.my_initializer = my_initializer
    self.my_initializer.current_step = None

    self.ui = uic.loadUi(f'ui/{my_initializer.lang}_{my_initializer.hand}_entry_step4.ui', self)
    self.button_yes.clicked.connect(self.yes_button_pressed)
    self.button_no.clicked.connect(self.no_button_pressed)

    # draw finger-tip cursor
    draw_finger_tip_cursor(self)
    # Hand tracking thread
    self.my_initializer.hand_position.connect(self.onHandPositionArrival)
    self.my_initializer.obj.reset_counter()
  
  def paintEvent(self, event):
    self.cursor_widget.move(self.finger_tip_x, self.finger_tip_y)
  
  # check if the button is touched
  def onHandPositionArrival(self, x, y, z, counter, cursor_x, cursor_y):
    # draw cursor for finger tip
    self.finger_tip_x = cursor_x
    self.finger_tip_y = cursor_y
    self.update()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_a) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_yes.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_b) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_no.click()

  @qtc.pyqtSlot()
  def yes_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = step4Ui.Step_4_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

  @qtc.pyqtSlot()
  def no_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.my_initializer.last_class = Entry_Step_4_UI
    self.target_ui = Menu_Default_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

########## Tutorial Ends UI class ##########
class Tutorial_Ends_UI(qtw.QWidget):
  def __init__(self, my_initializer):
    super().__init__()
    self.ui = uic.loadUi(f'ui/{my_initializer.lang}_xx_tutorial_ends.ui', self)
    self.button_exit.clicked.connect(self.exit_button_pressed)
    self.button_view.clicked.connect(self.button_view_clicked)
    # disable buttons
    self.button_exit.setEnabled(False)
    self.button_exit.setHidden(True)
    self.button_view.setEnabled(False)
    self.button_view.setHidden(True)
    self.widget_xp.setHidden(True)
    self.widget_score.setHidden(True)
    # pass on my_initializer
    self.my_initializer = my_initializer
    self.my_initializer.current_step = None
    # draw finger-tip cursor
    draw_finger_tip_cursor(self)
    # Hand tracking thread
    self.my_initializer.hand_position.connect(self.onHandPositionArrival)
    self.my_initializer.obj.reset_counter()

    # connect signals with functions
    self.my_initializer.obj_evaluator.first_delay_reached.connect(self.onFirstDelayReached)
    self.my_initializer.obj_evaluator.evaluation_result.connect(self.onEvaluationResult)
    if self.my_initializer.last_class == Tutorial_Ends_UI:
      # 1 - logic returned from menu UI
      self.label_party.setHidden(True)
      self.label_text_1.setHidden(True)
      self.label_text_2.setHidden(True)
      self.my_initializer.obj_evaluator.evaluation_result.emit(self.my_initializer.success_flag, self.my_initializer.difference_dict, self.my_initializer.score_dict, self.my_initializer.step_score_dict, self.my_initializer.step_score_sorted_list, self.my_initializer.overall_score_percentage)
    else:
      # 2 - logic continued from step 4 UI
      # close file
      self.my_initializer.obj_recorder.close_file()
      # archiving csv file - followed by creating new csv file
      self.my_initializer.archive_csv_name = self.my_initializer.obj_recorder.archive_old()
      # prepare for evaluation
      self.my_initializer.obj_evaluator.first_delay()

  def onFirstDelayReached(self):
    print("reaching point - first delay reached")  
    self.label_party.setHidden(True)
    self.my_initializer.obj_evaluator.evaluate(self.my_initializer.archive_csv_name, True)

  def onEvaluationResult(self, success_flag, difference_dict, score_dict, step_score_dict, step_score_sorted_list, overall_score_percentage):
    # save evaluation result in my_initializer
    self.my_initializer.success_flag = success_flag
    self.my_initializer.difference_dict = difference_dict
    self.my_initializer.score_dict = score_dict
    self.my_initializer.step_score_dict = step_score_dict
    self.my_initializer.step_score_sorted_list = step_score_sorted_list
    self.my_initializer.overall_score_percentage = overall_score_percentage
    # enable buttons
    self.button_exit.setEnabled(True)
    self.button_exit.setHidden(False)
    # show result
    if success_flag:
      print("reaching point - evaluation successful")
      # enable button_view
      self.button_view.setHidden(False)
      self.button_view.setEnabled(True)
      print('onEvaluationResult: overall_score_percentage:', overall_score_percentage)
      if overall_score_percentage*100 >= 80:
        # display texts upon high score
        if self.my_initializer.lang == 'en':
          self.label_text_1.setText("Congratulation! You performed almost like an expert.")
        else:
          self.label_text_1.setText("Glückwunsch! Sie sind fast wie ein Experte aufgetreten.")
      else:
        # step name with the lowest score
        if self.my_initializer.lang == 'en':
          self.label_text_1.setText(f"You seem to need more practice in {step_score_sorted_list[3][0]}.".replace('_', ' '))
        else:
          self.label_text_1.setText(f"Sie scheinen in {step_score_sorted_list[3][0]} mehr Übung zu brauchen.".replace('_', ' ').replace('step', 'Schritt'))
      # hints to touch the button
      if self.my_initializer.lang == 'en':
        self.label_text_2.setText("Touch the button below to view more details.")
      else:
        self.label_text_2.setText("Berühren Sie den unteren Knopf, um weitere Details anzusehen.")
      self.label_text_1.setHidden(False)
      self.label_text_2.setHidden(False)
      # to do - show score percentage
      self.label_text_score.setText(f"{int(overall_score_percentage*100)}%")
      self.widget_xp.setHidden(False)
      self.widget_score.setHidden(False)
    else:
      print("reaching point - evaluation not successful")
      # default - disable button_view
      self.button_view.setHidden(True)
      self.button_view.setEnabled(False)
      # debugging - enable button_view
      # self.button_view.setHidden(False)
      # self.button_view.setEnabled(True)
      if self.my_initializer.lang == 'en':
        self.label_text_1.setText("Sorry, we weren't able to process your gesture data, please connect mobile app and restart.")
      else:
        self.label_text_1.setText("Entschuldigung, wir konnten Ihre Gestendaten nicht verarbeiten, bitte verbinden Sie die mobile App und neustarten.")
      self.label_text_1.setHidden(False)
      self.label_text_2.setHidden(True)

  def paintEvent(self, event):
    self.cursor_widget.move(self.finger_tip_x, self.finger_tip_y)

  # check if the button is touched
  def onHandPositionArrival(self, x, y, z, counter, cursor_x, cursor_y):
    # draw cursor for finger tip
    self.finger_tip_x = cursor_x
    self.finger_tip_y = cursor_y
    self.update()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_b) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_exit.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_view) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_view.click()

  # check if button clicked
  def button_view_clicked(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = resUi.Result_StepX_PageX_UI(self.my_initializer, 1, 1)
    select_screen_and_show(self.target_ui)
    self.close()

  @qtc.pyqtSlot()
  def exit_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.my_initializer.last_class = Tutorial_Ends_UI
    self.target_ui = Menu_Default_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()


########## Menu Default UI class ##########
class Menu_Default_UI(qtw.QWidget):
  def __init__(self, my_initializer):
    super().__init__()
    # pass on my_initializer
    self.my_initializer = my_initializer
    self.my_initializer.current_step = None

    self.ui = uic.loadUi('ui/xx_xx_menu_default.ui', self)
    self.button_step1.clicked.connect(self.step1_button_pressed)
    self.button_step2.clicked.connect(self.step2_button_pressed)
    self.button_step3.clicked.connect(self.step3_button_pressed)
    self.button_step4.clicked.connect(self.step4_button_pressed)
    self.button_back.clicked.connect(self.back_button_pressed)
    self.button_restart.clicked.connect(self.restart_button_pressed)
    # draw finger-tip cursor
    draw_finger_tip_cursor(self)
    # Hand tracking thread
    self.my_initializer.hand_position.connect(self.onHandPositionArrival)
    self.my_initializer.obj.reset_counter()
  
  def paintEvent(self, event):
    self.cursor_widget.move(self.finger_tip_x, self.finger_tip_y)
  
  # check if the button is touched
  def onHandPositionArrival(self, x, y, z, counter, cursor_x, cursor_y):
    # draw cursor for finger tip
    self.finger_tip_x = cursor_x
    self.finger_tip_y = cursor_y
    self.update()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.step_1) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_step1.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.step_2) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_step2.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.step_3) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_step3.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.step_4) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_step4.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_c) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_back.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_d) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_restart.click()

  @qtc.pyqtSlot()
  def restart_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = Confirm_Restart_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()
  
  @qtc.pyqtSlot()
  def back_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    if self.my_initializer.last_class == resUi.Result_StepX_PageX_UI:
      self.target_ui = self.my_initializer.last_class(self.my_initializer, self.my_initializer.step_number, self.my_initializer.page_number)
    else:
      self.target_ui = self.my_initializer.last_class(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

  @qtc.pyqtSlot()
  def step1_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = Entry_Step_1_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

  @qtc.pyqtSlot()
  def step2_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = Entry_Step_2_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

  @qtc.pyqtSlot()
  def step3_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = Entry_Step_3_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

  @qtc.pyqtSlot()
  def step4_button_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = Entry_Step_4_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

########## Confirm Restart UI class ##########
class Confirm_Restart_UI(qtw.QWidget):
  def __init__(self, my_initializer):
    super().__init__()
    # pass on my_initializer
    self.my_initializer = my_initializer
    self.my_initializer.current_step = None

    self.ui = uic.loadUi(f'ui/xx_xx_confirm_restart.ui', self)
    self.button_yes.clicked.connect(self.restart_yes_pressed)
    self.button_no.clicked.connect(self.restart_no_pressed)
    
    # draw finger-tip cursor
    draw_finger_tip_cursor(self)
    # Hand tracking thread
    self.my_initializer.hand_position.connect(self.onHandPositionArrival)
    self.my_initializer.obj.reset_counter()
  
  def paintEvent(self, event):
    self.cursor_widget.move(self.finger_tip_x, self.finger_tip_y)
  
  # check if the button is touched
  def onHandPositionArrival(self, x, y, z, counter, cursor_x, cursor_y):
    # draw cursor for finger tip
    self.finger_tip_x = cursor_x
    self.finger_tip_y = cursor_y
    self.update()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_c) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_yes.click()
    if self.my_initializer.obj.button_positioner.check_in_area(x, y, z, self.my_initializer.obj.button_positioner.button_d) and self.my_initializer.obj.worker_activated and counter > self.my_initializer.interval_between_uis:
      self.button_no.click()
    
  @qtc.pyqtSlot()
  def restart_yes_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.my_initializer.obj_recorder.close_file()
    self.my_initializer.obj_recorder.archive_old()
    self.target_ui = FoodAssist(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()
  
  @qtc.pyqtSlot()
  def restart_no_pressed(self):
    self.my_initializer.hand_position.disconnect()
    self.target_ui = Menu_Default_UI(self.my_initializer)
    select_screen_and_show(self.target_ui)
    self.close()

# Helper Functions
def draw_finger_tip_cursor(self):
  self.finger_tip_x = 0
  self.finger_tip_y = 0
  self.cursor_widget = qtw.QWidget(self)
  cursor_layout = qtw.QHBoxLayout(self.cursor_widget)
  self.cursor_label = qtw.QLabel()
  self.cursor_label.setPixmap(qtg.QPixmap('ui/resources/Cursor.svg'))
  self.cursor_widget.setStyleSheet('background: transparent;')
  ### FIX me @ Didar
  # QCssParser::parseColorValue: Specified color without alpha value but alpha given: 'rgb 0, 0, 0, 0'
  # https://stackoverflow.com/questions/7667552/qt-widget-with-transparent-background
  ###
  cursor_layout.addWidget(self.cursor_label)
  self.cursor_widget.raise_()

# move the app to the secod screen (projector screen)
def select_screen_and_show(ui_class):
  screen_resolution = qtw.QApplication.desktop().screenGeometry(1)
  ui_class.move(qtc.QPoint(screen_resolution.x(), screen_resolution.y()))
  ui_class.showFullScreen()

def change_active_button_color(self, button):
  if button == 1:
    if self.findChild(qtw.QWidget, "button_sub_step2"):
      self.button_sub_step2.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_sub_step3"):
      self.button_sub_step3.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_sub_step4"):
      self.button_sub_step4.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step1"):
      self.button_step1.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step2"):
      self.button_step2.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step3"):
      self.button_step3.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step4"):
      self.button_step4.setStyleSheet('')
    self.button_sub_step1.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
  if button == 2:
    self.button_sub_step1.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_sub_step3"):
      self.button_sub_step3.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_sub_step4"):
      self.button_sub_step4.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step1"):
        self.button_step1.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step2"):
      self.button_step2.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step3"):
      self.button_step3.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step4"):
      self.button_step4.setStyleSheet('')
    self.button_sub_step2.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
  if button == 3:
    self.button_sub_step1.setStyleSheet('')
    self.button_sub_step2.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_sub_step4"):
      self.button_sub_step4.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step1"):
        self.button_step1.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step2"):
      self.button_step2.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step3"):
      self.button_step3.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step4"):
      self.button_step4.setStyleSheet('')
    self.button_sub_step3.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
  if button == 4:
    self.button_sub_step1.setStyleSheet('')
    self.button_sub_step2.setStyleSheet('')
    self.button_sub_step3.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step1"):
        self.button_step1.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step2"):
      self.button_step2.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step3"):
      self.button_step3.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step4"):
      self.button_step4.setStyleSheet('')
    self.button_sub_step4.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
  # All sub step button
  if button == 0:
    if self.findChild(qtw.QWidget, "button_sub_step1"):
      self.button_sub_step1.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_sub_step2"):
      self.button_sub_step2.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_sub_step3"):
      self.button_sub_step3.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_sub_step4"):
      self.button_sub_step4.setStyleSheet('')
    if self.findChild(qtw.QWidget, "button_step1"):
      self.button_step1.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
    if self.findChild(qtw.QWidget, "button_step2"):
      self.button_step2.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
    if self.findChild(qtw.QWidget, "button_step3"):
      self.button_step3.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
    if self.findChild(qtw.QWidget, "button_step4"):
      self.button_step4.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
  if button == 'de':
    self.button_de.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
    self.button_en.setStyleSheet('')
  if button == 'en':
    self.button_en.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
    self.button_de.setStyleSheet('')
  if button == 'left':
    self.button_left_shoulder.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
    self.button_right_shoulder.setStyleSheet('')
  if button == 'right':
    self.button_right_shoulder.setStyleSheet(open('./styles/activeButtonStyleGreen.css').read())
    self.button_left_shoulder.setStyleSheet('')

def on_substep_button_click(self, substep_button, all_substep=False):
  if not all_substep:
    # set counter to stop the thread when button is clicked
    self.counter = 99
  change_active_button_color(self, substep_button)
  self.player.setVideoOutput(self.ui.VideoWidget)
  self.playlist.setCurrentIndex(substep_button)
  self.player.setPosition(0)
  self.player.play()

def main():
  # initiate app
  app = qtw.QApplication([])
  # created initializer globally
  my_initializer = initializer.Initializer()
  target_ui = FoodAssist(my_initializer)
  select_screen_and_show(target_ui)

  # run the app
  sys.exit(app.exec_())
if __name__ == '__main__':
  main()
