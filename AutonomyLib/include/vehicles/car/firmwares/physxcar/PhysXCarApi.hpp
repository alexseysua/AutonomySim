// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

#ifndef autonomylib_vehicles_PhysXCarController_hpp
#define autonomylib_vehicles_PhysXCarController_hpp

#include "vehicles/car/api/CarApiBase.hpp"

namespace nervosys {
namespace autonomylib {

class PhysXCarApi : public CarApiBase {

  private:
    bool api_control_enabled_ = false;
    GeoPoint home_geopoint_;
    CarControls last_controls_;
    CarState last_car_state_;

  protected:
    virtual void resetImplementation() override { CarApiBase::resetImplementation(); }

  public:
    PhysXCarApi(const AutonomySimSettings::VehicleSetting *vehicle_setting,
                std::shared_ptr<SensorFactory> sensor_factory, const Kinematics::State &state,
                const Environment &environment)
        : CarApiBase(vehicle_setting, sensor_factory, state, environment),
          home_geopoint_(environment.getHomeGeoPoint()) {}

    ~PhysXCarApi() {}

    virtual void update() override { CarApiBase::update(); }

    virtual const SensorCollection &getSensors() const override { return CarApiBase::getSensors(); }

    // VehicleApiBase Implementation
    virtual void enableApiControl(bool is_enabled) override {
        if (api_control_enabled_ != is_enabled) {
            last_controls_ = CarControls();
            api_control_enabled_ = is_enabled;
        }
    }

    virtual bool isApiControlEnabled() const override { return api_control_enabled_; }

    virtual GeoPoint getHomeGeoPoint() const override { return home_geopoint_; }

    virtual bool armDisarm(bool arm) override {
        // TODO: implement arming for car
        unused(arm);
        return true;
    }

    virtual void setCarControls(const CarControls &controls) override { last_controls_ = controls; }

    virtual void updateCarState(const CarState &car_state) override { last_car_state_ = car_state; }

    virtual const CarState &getCarState() const override { return last_car_state_; }

    virtual const CarControls &getCarControls() const override { return last_controls_; }
};

} // namespace autonomylib
} // namespace nervosys

#endif
