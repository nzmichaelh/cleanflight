// Typedef to allow reuse of ranges and units.
// range: 1000...2000; units: ns
typedef int16_t servoDrive_t;

// Comment
// and more
typedef struct servoParam_s2 {
    // Short description.  Longer description to show in detailed
    // help.  Basics are inherited from the typedef.
    //
    // default: 1000
    servoDrive_t min;
    // default: 2000
    servoDrive_t max;
    // default: 1500
    servoDrive_t mid;
} foo_t;
