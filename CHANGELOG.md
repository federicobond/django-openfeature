Changelog
=========

## 0.2.0

 * Add `PROVIDER` key to the `OPENFEATURE` setting to configure the global
   OpenFeature provider declaratively (class path, factory function path,
   or provider instance), applied on app registry load and on
   `override_settings`

## 0.1.4

 * Drop support for python 3.8, 3.9, add support for 3.13, 3.14
 * Cache iffeature flag evaluation for the whole template

## 0.1.3

 * Various typing fixes

## 0.1.2

 * Fix missing `feature` template tag

## 0.1.1

 * Add `iffeature` template tag

## 0.1.0

 * Initial release
