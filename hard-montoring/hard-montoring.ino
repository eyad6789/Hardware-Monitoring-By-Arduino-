/*
 * Standalone Arduino PC Hardware Monitor
 * Generates simulated hardware data WITHOUT Python script
 * Displays on ILI9341 TFT LCD (240x320)
 * 
 * NOTE: This generates FAKE data for demonstration
 * Real PC hardware data requires communication with PC
 * 
 * Wiring for ILI9341 (SPI):
 * VCC -> 3.3V or 5V
 * GND -> GND
 * CS  -> Pin 10
 * RST -> Pin 9
 * DC  -> Pin 8
 * MOSI-> Pin 11
 * SCK -> Pin 13
 * LED -> 3.3V (backlight)
 */

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>

// TFT display pins
#define TFT_CS    10
#define TFT_RST   9
#define TFT_DC    8

// Create display object
Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_RST);

// Colors
#define BLACK     0x0000
#define WHITE     0xFFFF
#define RED       0xF800
#define GREEN     0x07E0
#define BLUE      0x001F
#define YELLOW    0xFFE0
#define CYAN      0x07FF
#define MAGENTA   0xF81F
#define ORANGE    0xFD20
#define DARKGREY  0x7BEF
#define LIGHTGREY 0xC618

// Hardware data structure
struct HardwareData {
  int cpuTemp;
  int gpuTemp;
  int cpuUsage;
  int ramUsage;
  int gpuUsage;
  int fps;
  unsigned long lastUpdate;
};

HardwareData hwData = {45, 55, 25, 60, 35, 120, 0};

// Display settings
const int DISPLAY_WIDTH = 240;
const int DISPLAY_HEIGHT = 320;
const int HEADER_HEIGHT = 30;
const int SECTION_HEIGHT = 45;
const int BAR_WIDTH = 180;
const int BAR_HEIGHT = 20;

// Timing
unsigned long lastDisplayUpdate = 0;
unsigned long lastDataUpdate = 0;
const unsigned long DISPLAY_UPDATE_INTERVAL = 500; // Update display every 500ms
const unsigned long DATA_UPDATE_INTERVAL = 1000;   // Update data every 1 second

// Simulation variables
float cpuTempBase = 45.0;
float gpuTempBase = 55.0;
float cpuUsageBase = 25.0;
float ramUsageBase = 60.0;
float gpuUsageBase = 35.0;
float fpsBase = 120.0;

void setup() {
  Serial.begin(9600);
  
  // Initialize TFT display
  tft.begin();
  tft.setRotation(0); // Portrait mode
  tft.fillScreen(BLACK);
  
  // Draw initial screen
  drawHeader();
  drawWelcomeMessage();
  
  Serial.println("Standalone Arduino PC Hardware Monitor");
  Serial.println("Generating simulated hardware data...");
  
  // Initialize random seed
  randomSeed(analogRead(0));
  
  delay(2000); // Show welcome message for 2 seconds
}

void loop() {
  // Update simulated data
  if (millis() - lastDataUpdate > DATA_UPDATE_INTERVAL) {
    updateSimulatedData();
    lastDataUpdate = millis();
  }
  
  // Update display
  if (millis() - lastDisplayUpdate > DISPLAY_UPDATE_INTERVAL) {
    updateDisplay();
    lastDisplayUpdate = millis();
  }
}

void updateSimulatedData() {
  // Simulate realistic hardware behavior
  
  // CPU Temperature: varies between 35-80°C
  cpuTempBase += random(-3, 4) * 0.5;
  cpuTempBase = constrain(cpuTempBase, 35, 80);
  hwData.cpuTemp = (int)cpuTempBase;
  
  // GPU Temperature: varies between 45-85°C
  gpuTempBase += random(-3, 4) * 0.5;
  gpuTempBase = constrain(gpuTempBase, 45, 85);
  hwData.gpuTemp = (int)gpuTempBase;
  
  // CPU Usage: varies between 10-95%
  cpuUsageBase += random(-10, 11) * 0.3;
  cpuUsageBase = constrain(cpuUsageBase, 10, 95);
  hwData.cpuUsage = (int)cpuUsageBase;
  
  // RAM Usage: varies between 40-90%
  ramUsageBase += random(-5, 6) * 0.2;
  ramUsageBase = constrain(ramUsageBase, 40, 90);
  hwData.ramUsage = (int)ramUsageBase;
  
  // GPU Usage: varies between 0-100%
  gpuUsageBase += random(-15, 16) * 0.4;
  gpuUsageBase = constrain(gpuUsageBase, 0, 100);
  hwData.gpuUsage = (int)gpuUsageBase;
  
  // FPS: varies between 30-144, influenced by GPU usage
  if (hwData.gpuUsage > 80) {
    fpsBase = 30 + random(0, 20); // Heavy load = lower FPS
  } else if (hwData.gpuUsage > 50) {
    fpsBase = 60 + random(0, 30); // Medium load
  } else {
    fpsBase = 100 + random(0, 44); // Light load = higher FPS
  }
  hwData.fps = (int)fpsBase;
  
  hwData.lastUpdate = millis();
  
  // Debug output
  Serial.print("CPU: ");
  Serial.print(hwData.cpuTemp);
  Serial.print("°C (");
  Serial.print(hwData.cpuUsage);
  Serial.print("%), GPU: ");
  Serial.print(hwData.gpuTemp);
  Serial.print("°C (");
  Serial.print(hwData.gpuUsage);
  Serial.print("%), RAM: ");
  Serial.print(hwData.ramUsage);
  Serial.print("%, FPS: ");
  Serial.println(hwData.fps);
}

void drawHeader() {
  tft.fillRect(0, 0, DISPLAY_WIDTH, HEADER_HEIGHT, BLUE);
  tft.setTextColor(WHITE);
  tft.setTextSize(2);
  tft.setCursor(10, 8);
  tft.println("PC Monitor");
  
  // Draw simulated connection status (always green)
  tft.fillCircle(DISPLAY_WIDTH - 20, 15, 6, GREEN);
  
  // Draw separator line
  tft.drawLine(0, HEADER_HEIGHT, DISPLAY_WIDTH, HEADER_HEIGHT, WHITE);
}

void drawWelcomeMessage() {
  tft.setTextColor(YELLOW);
  tft.setTextSize(1);
  tft.setCursor(10, 50);
  tft.println("DEMO MODE");
  
  tft.setTextColor(WHITE);
  tft.setCursor(10, 80);
  tft.println("Generating simulated");
  tft.setCursor(10, 95);
  tft.println("hardware data...");
  
  tft.setTextColor(CYAN);
  tft.setCursor(10, 120);
  tft.println("For real data:");
  tft.setCursor(10, 135);
  tft.println("Use Python script");
  tft.setCursor(10, 150);
  tft.println("with serial communication");
}

void updateDisplay() {
  // Clear main area (keep header)
  tft.fillRect(0, HEADER_HEIGHT + 1, DISPLAY_WIDTH, DISPLAY_HEIGHT - HEADER_HEIGHT - 1, BLACK);
  
  int yPos = HEADER_HEIGHT + 10;
  
  // Draw "DEMO MODE" indicator
  tft.setTextColor(YELLOW);
  tft.setTextSize(1);
  tft.setCursor(DISPLAY_WIDTH - 70, yPos);
  tft.println("DEMO MODE");
  yPos += 15;
  
  // CPU Temperature
  yPos += drawMetric("CPU Temp", hwData.cpuTemp, "C", yPos, true);
  
  // GPU Temperature  
  yPos += drawMetric("GPU Temp", hwData.gpuTemp, "C", yPos, true);
  
  // CPU Usage
  yPos += drawMetric("CPU Usage", hwData.cpuUsage, "%", yPos, false);
  
  // RAM Usage
  yPos += drawMetric("RAM Usage", hwData.ramUsage, "%", yPos, false);
  
  // GPU Usage
  yPos += drawMetric("GPU Usage", hwData.gpuUsage, "%", yPos, false);
  
  // FPS
  drawFPS(yPos);
  
  // Draw uptime
  drawUptime();
}

int drawMetric(String label, int value, String unit, int yPos, bool isTemperature) {
  // Draw label
  tft.setTextColor(WHITE);
  tft.setTextSize(1);
  tft.setCursor(10, yPos);
  tft.print(label);
  
  // Draw value
  tft.setTextSize(2);
  tft.setCursor(10, yPos + 12);
  
  // Color based on value
  uint16_t color = getValueColor(value, isTemperature);
  tft.setTextColor(color);
  tft.print(value);
  tft.print(unit);
  
  // Draw progress bar
  if (!isTemperature) {
    drawProgressBar(10, yPos + 30, BAR_WIDTH, 8, value, 100);
  } else {
    // For temperature, show bar from 30-90°C range
    int tempPercent = map(constrain(value, 30, 90), 30, 90, 0, 100);
    drawProgressBar(10, yPos + 30, BAR_WIDTH, 8, tempPercent, 100);
  }
  
  return SECTION_HEIGHT;
}

void drawFPS(int yPos) {
  tft.setTextColor(WHITE);
  tft.setTextSize(1);
  tft.setCursor(10, yPos);
  tft.print("FPS");
  
  tft.setTextSize(3);
  tft.setCursor(10, yPos + 12);
  
  // FPS color coding
  uint16_t fpsColor = GREEN;
  if (hwData.fps < 30) fpsColor = RED;
  else if (hwData.fps < 60) fpsColor = YELLOW;
  
  tft.setTextColor(fpsColor);
  tft.print(hwData.fps);
  
  // Draw FPS category
  tft.setTextSize(1);
  tft.setTextColor(WHITE);
  tft.setCursor(120, yPos + 20);
  if (hwData.fps >= 120) tft.print("HIGH");
  else if (hwData.fps >= 60) tft.print("GOOD");
  else if (hwData.fps >= 30) tft.print("OK");
  else tft.print("LOW");
}

void drawProgressBar(int x, int y, int width, int height, int value, int maxValue) {
  int fillWidth = map(value, 0, maxValue, 0, width);
  
  // Draw border
  tft.drawRect(x, y, width, height, WHITE);
  
  // Draw filled portion
  uint16_t fillColor = getValueColor(value, false);
  if (fillWidth > 2) {
    tft.fillRect(x + 1, y + 1, fillWidth - 2, height - 2, fillColor);
  }
  
  // Draw empty portion
  if (fillWidth < width - 1) {
    tft.fillRect(x + fillWidth, y + 1, width - fillWidth - 1, height - 2, BLACK);
  }
}

uint16_t getValueColor(int value, bool isTemperature) {
  if (isTemperature) {
    // Temperature color coding
    if (value >= 80) return RED;
    else if (value >= 70) return ORANGE;
    else if (value >= 60) return YELLOW;
    else return GREEN;
  } else {
    // Usage percentage color coding
    if (value >= 90) return RED;
    else if (value >= 70) return ORANGE;
    else if (value >= 50) return YELLOW;
    else return GREEN;
  }
}

void drawUptime() {
  unsigned long uptimeSeconds = millis() / 1000;
  unsigned long uptimeMinutes = uptimeSeconds / 60;
  unsigned long uptimeHours = uptimeMinutes / 60;
  
  uptimeSeconds %= 60;
  uptimeMinutes %= 60;
  
  tft.setTextColor(DARKGREY);
  tft.setTextSize(1);
  tft.setCursor(10, DISPLAY_HEIGHT - 15);
  tft.print("Uptime: ");
  tft.print(uptimeHours);
  tft.print("h ");
  tft.print(uptimeMinutes);
  tft.print("m ");
  tft.print(uptimeSeconds);
  tft.print("s");
}

// Alternative function to read REAL data from serial
void readRealDataFromSerial() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    
    if (data.length() > 0) {
      parseRealData(data);
    }
  }
}

void parseRealData(String data) {
  // Parse CSV format: CPU_Temp,GPU_Temp,CPU_Usage,RAM_Usage,GPU_Usage,FPS
  int values[6];
  int valueIndex = 0;
  int lastIndex = 0;
  
  // Split by comma
  for (int i = 0; i <= data.length(); i++) {
    if (data.charAt(i) == ',' || i == data.length()) {
      if (valueIndex < 6) {
        String valueStr = data.substring(lastIndex, i);
        values[valueIndex] = valueStr.toInt();
        valueIndex++;
        lastIndex = i + 1;
      }
    }
  }
  
  // Update hardware data if we got all 6 values
  if (valueIndex == 6) {
    hwData.cpuTemp = constrain(values[0], 0, 100);
    hwData.gpuTemp = constrain(values[1], 0, 100);
    hwData.cpuUsage = constrain(values[2], 0, 100);
    hwData.ramUsage = constrain(values[3], 0, 100);
    hwData.gpuUsage = constrain(values[4], 0, 100);
    hwData.fps = constrain(values[5], 0, 999);
    hwData.lastUpdate = millis();
    
    Serial.println("Real data received from PC!");
  }
}