enum PGN {
    MSP_API_VERSION = 1,    //out message
    MSP_FC_VARIANT = 2,    //out message
    MSP_FC_VERSION = 3,    //out message
    MSP_BOARD_INFO = 4,    //out message
    MSP_BUILD_INFO = 5,    //out message

//
// MSP commands for Cleanflight original features
//
    MSP_MISSING_CHANNEL_FORWARDING = 32,    //out message         Returns channel forwarding settings
    MSP_SET_CHANNEL_FORWARDING = 33,    //in message          Channel forwarding settings

    MSP_MODE_RANGES = 34,    //out message         Returns all mode ranges
    MSP_SET_MODE_RANGE = 35,    //in message          Sets a single mode range

    MSP_FEATURE = 36,
    MSP_SET_FEATURE = 37,

    MSP_BOARD_ALIGNMENT = 38,
    MSP_SET_BOARD_ALIGNMENT = 39,

    MSP_CURRENT_METER_CONFIG = 40,
    MSP_SET_CURRENT_METER_CONFIG = 41,

    MSP_MIXER = 42,
    MSP_SET_MIXER = 43,

    MSP_RX_CONFIG = 44,
    MSP_SET_RX_CONFIG = 45,

    MSP_LED_COLORS = 46,
    MSP_SET_LED_COLORS = 47,

    MSP_LED_STRIP_CONFIG = 48,
    MSP_SET_LED_STRIP_CONFIG = 49,

    MSP_RSSI_CONFIG = 50,
    MSP_SET_RSSI_CONFIG = 51,

    MSP_ADJUSTMENT_RANGES = 52,
    MSP_SET_ADJUSTMENT_RANGE = 53,

// private - only to be used by the configurator, the commands are likely to change
    MSP_CF_SERIAL_CONFIG = 54,
    MSP_SET_CF_SERIAL_CONFIG = 55,

    MSP_VOLTAGE_METER_CONFIG = 56,
    MSP_SET_VOLTAGE_METER_CONFIG = 57,

    MSP_SONAR_ALTITUDE = 58, //out message get sonar altitude [cm]

    MSP_PID_CONTROLLER = 59,
    MSP_SET_PID_CONTROLLER = 60,

    MSP_ARMING_CONFIG = 61, //out message         Returns auto_disarm_delay and disarm_kill_switch parameters
    MSP_SET_ARMING_CONFIG = 62, //in message          Sets auto_disarm_delay and disarm_kill_switch parameters

    MSP_DATAFLASH_SUMMARY = 70, //out message - get description of dataflash chip
    MSP_DATAFLASH_READ = 71, //out message - get content of dataflash chip
    MSP_DATAFLASH_ERASE_CMD = 72, //in message - erase dataflash chip

    MSP_LOOP_TIME = 73, //out message         Returns FC cycle time i.e looptime parameter
    MSP_SET_LOOP_TIME = 74, //in message          Sets FC cycle time i.e looptime parameter

    MSP_MISSING_FAILSAFE_CONFIG = 75, //out message         Returns FC Fail-Safe settings
    MSP_SET_FAILSAFE_CONFIG = 76, //in message          Sets FC Fail-Safe settings
//
// Baseflight MSP commands (if enabled they exist in Cleanflight)
//
    MSP_RX_MAP = 64, //out message get channel map (also returns number of channels total)
    MSP_SET_RX_MAP = 65, //in message set rx map, numchannels to set comes from MSP_RX_MAP

// FIXME - Provided for backwards compatibility with configurator code until configurator is updated.
// DEPRECATED - DO NOT USE "MSP_BF_CONFIG" and MSP_SET_BF_CONFIG.  In Cleanflight, isolated commands already exist and should be used instead.
    MSP_BF_CONFIG = 66, //out message baseflight-specific settings that aren't covered elsewhere
    MSP_SET_BF_CONFIG = 67, //in message baseflight-specific settings save

    MSP_REBOOT_CMD = 68, //in message reboot settings

// DEPRECATED - Use MSP_BUILD_INFO instead
    MSP_BF_BUILD_INFO = 69, //out message build date as well as some space for future expansion

//
// Multwii original MSP commands
//

// DEPRECATED - See MSP_API_VERSION and MSP_MIXER
    MSP_IDENT = 100,    //out message         mixerMode + multiwii version + protocol version + capability variable


    MSP_STATUS = 101,    //out message         cycletime & errors_count & sensor present & box activation & current setting number
    MSP_RAW_IMU = 102,    //out message         9 DOF
    MSP_SERVO = 103,    //out message         8 servos
    MSP_MOTOR = 104,    //out message         8 motors
    MSP_RC = 105,    //out message         8 rc chan and more
    MSP_RAW_GPS = 106,    //out message         fix, numsat, lat, lon, alt, speed, ground course
    MSP_COMP_GPS = 107,    //out message         distance home, direction home
    MSP_ATTITUDE = 108,    //out message         2 angles 1 heading
    MSP_ALTITUDE = 109,    //out message         altitude, variometer
    MSP_ANALOG = 110,    //out message         vbat, powermetersum, rssi if available on RX
    MSP_RC_TUNING = 111,    //out message         rc rate, rc expo, rollpitch rate, yaw rate, dyn throttle PID
    MSP_PID = 112,    //out message         P I D coeff (9 are used currently)
    MSP_MISSING_BOX = 113,    //out message         BOX setup (number is dependant of your setup)
    MSP_MISC = 114,    //out message         powermeter trig
    MSP_MOTOR_PINS = 115,    //out message         which pins are in use for motors & servos, for GUI
    MSP_BOXNAMES = 116,    //out message         the aux switch names
    MSP_PIDNAMES = 117,    //out message         the PID names
    MSP_WP = 118,    //out message         get a WP, WP# is in the payload, returns (WP#, lat, lon, alt, flags) WP#0-home, WP#16-poshold
    MSP_BOXIDS = 119,    //out message         get the permanent IDs associated to BOXes
    MSP_SERVO_CONFIGURATIONS = 120,    //out message         All servo configurations.
    MSP_MISSING_NAV_STATUS = 121,    //out message         Returns navigation status
    MSP_MISSING_NAV_CONFIG = 122,    //out message         Returns navigation parameters

    MSP_SET_RAW_RC = 200,    //in message          8 rc chan
    MSP_SET_RAW_GPS = 201,    //in message          fix, numsat, lat, lon, alt, speed
    MSP_SET_PID = 202,    //in message          P I D coeff (9 are used currently)
    MSP_SET_BOX = 203,    //in message          BOX setup (number is dependant of your setup)
    MSP_SET_RC_TUNING = 204,    //in message          rc rate, rc expo, rollpitch rate, yaw rate, dyn throttle PID, yaw expo
    MSP_ACC_CALIBRATION_CMD = 205,    //in message          no param
    MSP_MAG_CALIBRATION_CMD = 206,    //in message          no param
    MSP_SET_MISC = 207,    //in message          powermeter trig + 8 free for future use
    MSP_RESET_CONF_CMD = 208,    //in message          no param
    MSP_SET_WP = 209,    //in message          sets a given WP (WP#,lat, lon, alt, flags)
    MSP_SELECT_SETTING_CMD = 210,    //in message          Select Setting Number (0-2)
    MSP_SET_HEAD = 211,    //in message          define a new heading hold direction
    MSP_SET_SERVO_CONFIGURATION = 212,    //in message          Servo settings
    MSP_SET_MOTOR = 214,    //in message          PropBalance function
    MSP_SET_NAV_CONFIG = 215,    //in message          Sets nav config parameters - write to the eeprom

    MSP_BIND = 240,    //in message          no param

    MSP_EEPROM_WRITE_CMD = 250,    //in message          no param

    MSP_DEBUGMSG = 253,    //out message         debug string buffer
    MSP_DEBUG = 254,    //out message         debug1,debug2,debug3,debug4

// Additional commands that are not compatible with MultiWii
    MSP_UID = 160,    //out message         Unique device ID
    MSP_ACC_TRIM = 240,    //out message         get acc angle trim values
    MSP_SET_ACC_TRIM = 239,    //in message          set acc angle trim values
    MSP_GPSSVINFO = 164,    //out message         get Signal Strength (only U-Blox)
    MSP_SERVO_MIX_RULES = 241,    //out message         Returns servo mixer configuration
    MSP_SET_SERVO_MIX_RULE = 242,    //in message          Sets servo mixer configuration
};

// pgn: MSP_API_VERSION
// size: 1 + API_VERSION_LENGTH;
struct mspApiVersion_s {
    uint8_t mspProtocolVersion;

    uint8_t apiVersionMajor;
    uint8_t apiVersionMinor;
};
// pgn: MSP_FC_VARIANT
// size: FLIGHT_CONTROLLER_IDENTIFIER_LENGTH;
struct mspFcVariant_s {

    char flightControllerIdentifier[4];
};
// pgn: MSP_FC_VERSION
// size: FLIGHT_CONTROLLER_VERSION_LENGTH;
struct mspFcVersion_s {

    uint8_t fcVersionMajor;
    uint8_t fcVersionMinor;
    uint8_t fcVersionPatchLevel;
};
// pgn: MSP_BOARD_INFO
// size: BOARD_IDENTIFIER_LENGTH + BOARD_HARDWARE_REVISION_LENGTH;
struct mspBoardInfo_s {
    char boardIdentifier[4];
    uint16_t hardwareRevision;
};
// pgn: MSP_BUILD_INFO
// size: BUILD_DATE_LENGTH + BUILD_TIME_LENGTH + GIT_SHORT_REVISION_LENGTH
struct mspBuildInfo_s {
    char buildDate[11];
    char buildTime[8];
    char shortGitRevision[7];
};
// pgn: MSP_IDENT
// size: 7;
struct mspIdent_s {
    uint8_t mwVersion;
    uint8_t mixerMode;
    uint8_t mspProtocolVersion;
    uint32_t capDynbalance; // "capability"
};
// pgn: MSP_STATUS
// size: 11;
struct mspStatus_s {
    uint16_t cycleTime;
    uint16_t i2cGetErrorCounter;
    uint16_t sensors;
    uint32_t junk;
    uint8_t currentProfileIndex;
};
// pgn: MSP_RAW_IMU
// size: 18;
struct mspRawImu_s {

    int16_t accSmooth[3];
    int16_t gyroADC[3];
    int16_t magADC[3];
};
// pgn: MSP_SERVO
struct mspServo_s {
    int16_t servo[];
};
// pgn: MSP_SERVO_CONFIGURATIONS
struct mspServoConfigurations_s {
    struct {
        uint16_t min;
        uint16_t max;
        uint16_t middle;
        uint8_t rate;
        uint8_t angleAtMin;
        uint8_t angleAtMax;
        int8_t forwardFromChannel;
        uint32_t reversedSources;
    } servo[];
};
// pgn: MSP_SERVO_MIX_RULES
struct mspServoMixRules_s {
    // PENDING: Repeats.
    uint8_t targetChannel;
    uint8_t inputSource;
    uint8_t rate;
    uint8_t speed;
    uint8_t min;
    uint8_t max;
    uint8_t box;
};
// pgn: MSP_MOTOR
struct mspMotor_s {
    int16_t motor[];
};
// pgn: MSP_RC
struct mspRc_s {
    uint16_t rcData[];
};
// pgn: MSP_ATTITUDE
// size: 6;
struct mspAttitude_s {
    int16_t inclination[2];
    int16_t heading;
};
// pgn: MSP_ALTITUDE
// size: 6;
struct mspAltitude_s {
    int32_t altitudeHoldGetEstimatedAltitude;
    int16_t vario;
};
// pgn: MSP_SONAR_ALTITUDE
// size: 4;
struct mspSonarAltitude_s {
    uint32_t sonarGetLatestAltitude;
};
// pgn: MSP_ANALOG
// size: 7;
struct mspAnalog_s {
    uint8_t vbat;
    uint16_t mAhDrawn;
    uint16_t rssi;
    uint16_t amperage;
};
// pgn: MSP_ARMING_CONFIG
// size: 2;
struct mspArmingConfig_s {
    uint8_t autoDisarmDelay;
    uint8_t disarmKillSwitch;
};
// pgn: MSP_LOOP_TIME
// size: 2;
struct mspLoopTime_s {
    uint16_t looptime;
};
// pgn: MSP_RC_TUNING
// size: 11;
struct mspRcTuning_s {
    uint8_t rcRate8;
    uint8_t rcExpo8;
    uint8_t rates[3];
    uint8_t dynThrPID;
    uint8_t thrMid8;
    uint8_t thrExpo8;
    uint16_t tpaBreakpoint;
    uint8_t rcYawExpo8;
};
// pgn: MSP_PID
// size: 3 * PID_ITEM_COUNT;
struct mspPid_s {
    // PENDING: Repeats.
    uint8_t kp;
    uint8_t ki;
    uint8_t kd;
};
// pgn: MSP_PIDNAMES
// size: sizeof(pidnames - 1);
struct mspPidNames_s {
    char pidnames[];
};
// pgn: MSP_PID_CONTROLLER
// size: 1;
struct mspPidController_s {
    uint8_t pidController;
};
// pgn: MSP_MODE_RANGES
struct mspModeRanges_s {
    // PENDING: Repeats.
    uint8_t permanentId;
    uint8_t auxChannelIndex;
    uint8_t startStep;
    uint8_t endStep;
};
// pgn: MSP_ADJUSTMENT_RANGES
struct mspAdjustmentRanges_s {
    // PENDING: Repeats.
    uint8_t adjustmentIndex;
    uint8_t auxChannelIndex;
    uint8_t startStep;
    uint8_t endStep;
    uint8_t adjustmentFunction;
    uint8_t auxSwitchChannelIndex;
};
// pgn: MSP_BOXNAMES
struct mspBoxnames_s {
    // PENDING.
    char names[];
};
// pgn: MSP_BOXIDS
struct mspBoxids_s {
    uint8_t permanentId[];
};
// pgn: MSP_MISC
// size: 2 * 5 + 3 + 3 + 2 + 4;
struct mspMisc_s {
    uint16_t midrc;

    uint16_t minthrottle;
    uint16_t maxthrottle;
    uint16_t mincommand;

    uint16_t failsafeThrottle;

    uint8_t gpsType;     // gps_type
    uint8_t gpsBaudrate; // TODO gps_baudrate (an index, cleanflight uses a
                          // uint32_t
    uint8_t sbasMode;     // gps_ubx_sbas
    uint8_t multiwiiCurrentMeterOutput;
    uint8_t channel;
    uint8_t zero2;

    uint16_t magDeclination;

    uint8_t vbatscale;
    uint8_t vbatmincellvoltage;
    uint8_t vbatmaxcellvoltage;
    uint8_t vbatwarningcellvoltage;
};
// pgn: MSP_MOTOR_PINS
struct mspMotorPins_s {
    uint8_t pins[8];
};
// pgn: MSP_RAW_GPS
// size: 16;
struct mspRawGps_s {
    uint8_t state;
    uint8_t numSat;
    uint32_t lat;
    uint32_t lon;
    uint16_t gpsAltitude;
    uint16_t gpsSpeed;
    uint16_t gpsGround_course;
};
// pgn: MSP_COMP_GPS
// size: 5;
struct mspCompGps_s {
    uint16_t gpsDistanceToHome;
    uint16_t gpsDirectionToHome;
    uint8_t gpsUpdate;
};
// pgn: MSP_WP
// size: 18;
struct mspWp_s {
    // PENDING: indexed.

    uint8_t wpNo;
    uint32_t lat;
    uint32_t lon;
    uint32_t altHold;    // altitude (cm) will come here -- temporary
                         // implementation to test feature with apps
    uint16_t heading;    // heading  will come here (deg)
    uint16_t timeToStay; // time to stay (ms) will come here
    uint8_t navFlag;     // nav flag will come here
};
// pgn: MSP_GPSSVINFO
// size: 1 + (GPS_numCh * 4);
struct mspGpssvinfo_s {
    // PENDING: Repeats.
    uint8_t chn;
    uint8_t svid;
    uint8_t quality;
    uint8_t cno;
};
// pgn: MSP_DEBUG
// size: DEBUG16_VALUE_COUNT * sizeof(debug[0]);
struct mspDebug_s {
    uint16_t debug[]; // 4 variables are here for general monitoring purpose
};
// pgn: MSP_ACC_TRIM
// size: 4;
struct mspAccTrim_s {
    uint16_t pitch;
    uint16_t roll;
};
// pgn: MSP_UID
// size: 12;
struct mspUID_s {
    uint32_t id[3];
};

typedef enum {
    FEATURE_RX_PPM = 1 << 0,
    FEATURE_VBAT = 1 << 1,
    FEATURE_INFLIGHT_ACC_CAL = 1 << 2,
    FEATURE_RX_SERIAL = 1 << 3,
    FEATURE_MOTOR_STOP = 1 << 4,
    FEATURE_SERVO_TILT = 1 << 5,
    FEATURE_SOFTSERIAL = 1 << 6,
    FEATURE_GPS = 1 << 7,
    FEATURE_FAILSAFE = 1 << 8,
    FEATURE_SONAR = 1 << 9,
    FEATURE_TELEMETRY = 1 << 10,
    FEATURE_CURRENT_METER = 1 << 11,
    FEATURE_3D = 1 << 12,
    FEATURE_RX_PARALLEL_PWM = 1 << 13,
    FEATURE_RX_MSP = 1 << 14,
    FEATURE_RSSI_ADC = 1 << 15,
    FEATURE_LED_STRIP = 1 << 16,
    FEATURE_DISPLAY = 1 << 17,
    FEATURE_ONESHOT125 = 1 << 18,
    FEATURE_BLACKBOX = 1 << 19,
    FEATURE_CHANNEL_FORWARDING = 1 << 20
} features_e;

// pgn: MSP_FEATURE
// size: 4;
struct mspFeature_s {
    uint32_t featureMask;
};
// pgn: MSP_BOARD_ALIGNMENT
struct mspBoardAlignment_s {
    int16_t rollDegrees;
    int16_t pitchDegrees;
    int16_t yawDegrees;
};
// pgn: MSP_VOLTAGE_METER_CONFIG
// size: 4;
struct mspVoltageMeterConfig_s {
    uint8_t vbatscale;
    uint8_t vbatmincellvoltage;
    uint8_t vbatmaxcellvoltage;
    uint8_t vbatwarningcellvoltage;
};
// pgn: MSP_CURRENT_METER_CONFIG
// size: 7;
struct mspCurrentMeterConfig_s {
    uint16_t currentMeterScale;
    uint16_t currentMeterOffset;
    uint8_t currentMeterType;
    uint16_t batteryCapacity;
};
// pgn: MSP_MIXER
// size: 1;
struct mspMixer_s {
    // type: mixerMode_e
    uint8_t mixerMode;
};
// pgn: MSP_RX_CONFIG
// size: 12;
struct mspRxConfig_s {
    uint8_t serialrxProvider;
    uint16_t maxcheck;
    uint16_t midrc;
    uint16_t mincheck;
    uint8_t spektrumSatBind;
    uint16_t rxMinUsec;
    uint16_t rxMaxUsec;
};
// pgn: MSP_RSSI_CONFIG
// size: 1;
struct mspRssiConfig_s {
    uint8_t channel;
};
// pgn: MSP_RX_MAP
// size: MAX_MAPPABLE_RX_INPUTS;
struct mspRxMap_s {
    uint8_t rcmap[];
};

enum mixerMode_e
{
    MIXER_TRI = 1,
    MIXER_QUADP = 2,
    MIXER_QUADX = 3,
    MIXER_BICOPTER = 4,
    MIXER_GIMBAL = 5,
    MIXER_Y6 = 6,
    MIXER_HEX6 = 7,
    MIXER_FLYING_WING = 8,
    MIXER_Y4 = 9,
    MIXER_HEX6X = 10,
    MIXER_OCTOX8 = 11,
    MIXER_OCTOFLATP = 12,
    MIXER_OCTOFLATX = 13,
    MIXER_AIRPLANE = 14,        // airplane / singlecopter / dualcopter (not yet properly supported)
    MIXER_HELI_120_CCPM = 15,
    MIXER_HELI_90_DEG = 16,
    MIXER_VTAIL4 = 17,
    MIXER_HEX6H = 18,
    MIXER_PPM_TO_SERVO = 19,    // PPM -> servo relay
    MIXER_DUALCOPTER = 20,
    MIXER_SINGLECOPTER = 21,
    MIXER_ATAIL4 = 22,
    MIXER_CUSTOM = 23,
    MIXER_CUSTOM_AIRPLANE = 24,
    MIXER_CUSTOM_TRI = 25
};

enum features_e {
    FEATURE_RX_PPM = 1 << 0,
    FEATURE_VBAT = 1 << 1,
    FEATURE_INFLIGHT_ACC_CAL = 1 << 2,
    FEATURE_RX_SERIAL = 1 << 3,
    FEATURE_MOTOR_STOP = 1 << 4,
    FEATURE_SERVO_TILT = 1 << 5,
    FEATURE_SOFTSERIAL = 1 << 6,
    FEATURE_GPS = 1 << 7,
    FEATURE_FAILSAFE = 1 << 8,
    FEATURE_SONAR = 1 << 9,
    FEATURE_TELEMETRY = 1 << 10,
    FEATURE_CURRENT_METER = 1 << 11,
    FEATURE_3D = 1 << 12,
    FEATURE_RX_PARALLEL_PWM = 1 << 13,
    FEATURE_RX_MSP = 1 << 14,
    FEATURE_RSSI_ADC = 1 << 15,
    FEATURE_LED_STRIP = 1 << 16,
    FEATURE_DISPLAY = 1 << 17,
    FEATURE_ONESHOT125 = 1 << 18,
    FEATURE_BLACKBOX = 1 << 19,
    FEATURE_CHANNEL_FORWARDING = 1 << 20
};

enum serialRXType_e {
    SERIALRX_SPEKTRUM1024 = 0,
    SERIALRX_SPEKTRUM2048 = 1,
    SERIALRX_SBUS = 2,
    SERIALRX_SUMD = 3,
    SERIALRX_SUMH = 4,
    SERIALRX_XBUS_MODE_B = 5,
    SERIALRX_XBUS_MODE_B_RJ01 = 6,
};

// pgn: MSP_BF_CONFIG
// size: 1 + 4 + 1 + 2 + 2 + 2 + 2 + 2;
struct mspBfConfig_s {
    // type: mixerMode_e
    uint8_t mixerMode;

    // type: features_e
    uint32_t featureMask;

    // type: serialRXType_e
    uint8_t serialrxProvider;

    uint16_t rollDegrees;
    uint16_t pitchDegrees;
    uint16_t yawDegrees;

    uint16_t currentMeterScale;
    uint16_t currentMeterOffset;
};
// pgn: MSP_CF_SERIAL_CONFIG
struct mspCfSerialConfig_s {
    // PENDING: Repeats.
    uint8_t identifier;
    uint16_t functionMask;
    uint8_t mspBaudrateIndex;
    uint8_t gpsBaudrateIndex;
    uint8_t telemetryBaudrateIndex;
    uint8_t blackboxBaudrateIndex;
};

// pgn: MSP_LED_COLORS
struct mspLedColors_s {
    // PENDING: Repeats.
    uint16_t h;
    uint8_t s;
    uint8_t v;
};

// pgn: MSP_LED_STRIP_CONFIG
struct mspLedStripConfig_s {
    // PENDING: Repeats.
    uint16_t direction;
    uint16_t function;
    uint8_t x;
    uint8_t y;
    uint8_t color;
};
// pgn: MSP_DATAFLASH_SUMMARY
struct mspDataflashSummary_s {
    uint8_t isReady;
    uint32_t sectors;
    uint32_t totalSize;
    uint32_t offset;
};
// pgn: MSP_DATAFLASH_READ
struct mspDataflashRead_s {
    uint32_t address;
    uint8_t data[];
};
// Build info.
// pgn: MSP_BF_BUILD_INFO
// size: 11 + 4 + 4;
struct mspBfBuildInfo_s {
    uint8_t buildData[11];
    uint32_t reserved1; // future exp
    uint32_t reserved2; // future exp
};

// pgn: MSP_DEBUGMSG
struct mspDebugMsg_s {
    char msg[];
};
// pgn: MSP_SET_SERVO_CONFIGURATION
struct mspSetServoConfiguration_s {
    uint8_t idx;
    int16_t min;                            // servo min
    int16_t max;                            // servo max
    int16_t middle;                         // servo middle
    int8_t rate;                            // range [-125;+125] ; can be used to adjust a rate 0-125% and a direction
    uint8_t angleAtMin;                     // range [0;180] the measured angle in degrees from the middle when the servo is at the 'min' value.
    uint8_t angleAtMax;                     // range [0;180] the measured angle in degrees from the middle when the servo is at the 'max' value.
    // PENDING: signed or unsigned?
    int8_t forwardFromChannel;              // RX channel index, 0 based.  See CHANNEL_FORWARDING_DISABLED
    uint32_t reversedSources;               // the direction of servo movement for each input source of the servo mixer, bit set=inverted
};
