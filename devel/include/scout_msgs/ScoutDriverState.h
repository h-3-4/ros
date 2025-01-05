// Generated by gencpp from file scout_msgs/ScoutDriverState.msg
// DO NOT EDIT!


#ifndef SCOUT_MSGS_MESSAGE_SCOUTDRIVERSTATE_H
#define SCOUT_MSGS_MESSAGE_SCOUTDRIVERSTATE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace scout_msgs
{
template <class ContainerAllocator>
struct ScoutDriverState_
{
  typedef ScoutDriverState_<ContainerAllocator> Type;

  ScoutDriverState_()
    : driver_voltage(0.0)
    , driver_temperature(0.0)
    , driver_state(0)  {
    }
  ScoutDriverState_(const ContainerAllocator& _alloc)
    : driver_voltage(0.0)
    , driver_temperature(0.0)
    , driver_state(0)  {
  (void)_alloc;
    }



   typedef double _driver_voltage_type;
  _driver_voltage_type driver_voltage;

   typedef double _driver_temperature_type;
  _driver_temperature_type driver_temperature;

   typedef uint8_t _driver_state_type;
  _driver_state_type driver_state;





  typedef boost::shared_ptr< ::scout_msgs::ScoutDriverState_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::scout_msgs::ScoutDriverState_<ContainerAllocator> const> ConstPtr;

}; // struct ScoutDriverState_

typedef ::scout_msgs::ScoutDriverState_<std::allocator<void> > ScoutDriverState;

typedef boost::shared_ptr< ::scout_msgs::ScoutDriverState > ScoutDriverStatePtr;
typedef boost::shared_ptr< ::scout_msgs::ScoutDriverState const> ScoutDriverStateConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::scout_msgs::ScoutDriverState_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::scout_msgs::ScoutDriverState_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace scout_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'scout_msgs': ['/home/hdh/catkin_ws/src/scout_ros/scout_msgs/msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::scout_msgs::ScoutDriverState_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::scout_msgs::ScoutDriverState_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::scout_msgs::ScoutDriverState_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::scout_msgs::ScoutDriverState_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::scout_msgs::ScoutDriverState_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::scout_msgs::ScoutDriverState_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::scout_msgs::ScoutDriverState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "bcb2bfdfab7869cfb37bcfdc3a86c1d4";
  }

  static const char* value(const ::scout_msgs::ScoutDriverState_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xbcb2bfdfab7869cfULL;
  static const uint64_t static_value2 = 0xb37bcfdc3a86c1d4ULL;
};

template<class ContainerAllocator>
struct DataType< ::scout_msgs::ScoutDriverState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "scout_msgs/ScoutDriverState";
  }

  static const char* value(const ::scout_msgs::ScoutDriverState_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::scout_msgs::ScoutDriverState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64 driver_voltage\n\
float64 driver_temperature\n\
uint8   driver_state\n\
";
  }

  static const char* value(const ::scout_msgs::ScoutDriverState_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::scout_msgs::ScoutDriverState_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.driver_voltage);
      stream.next(m.driver_temperature);
      stream.next(m.driver_state);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct ScoutDriverState_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::scout_msgs::ScoutDriverState_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::scout_msgs::ScoutDriverState_<ContainerAllocator>& v)
  {
    s << indent << "driver_voltage: ";
    Printer<double>::stream(s, indent + "  ", v.driver_voltage);
    s << indent << "driver_temperature: ";
    Printer<double>::stream(s, indent + "  ", v.driver_temperature);
    s << indent << "driver_state: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.driver_state);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SCOUT_MSGS_MESSAGE_SCOUTDRIVERSTATE_H