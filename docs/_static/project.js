/*
 * Sidebar decoration that belongs to this project's content: icons of the modules and
 * pages, and the page classes that select the icon style. The theme (theme/) reads this
 * object; see theme/README.md for the format.
 */
window.AGILE_DOCS_CONFIG = {
  // [path suffix, image under _static, label]
  navIconImages: [
    ['/cpp/index.html', 'icons/cpp.svg', 'C++'],
    ['/python/index.html', 'icons/python.svg', 'Python'],
    ['/fci/examples/cpp/index.html', 'icons/cpp.svg', 'C++'],
    ['/fci/examples/python/index.html', 'icons/python.svg', 'Python'],
    ['/fci/index.html', 'icons/franka-arm.svg', 'FCI'],
    ['/ros2/index.html', 'icons/ros2.svg', 'ROS 2'],
    ['/ros2/humble/index.html', 'icons/ros2-humble.svg', 'ROS 2 Humble'],
    ['/ros2/jazzy/index.html', 'icons/ros2-jazzy.svg', 'ROS 2 Jazzy'],
  ],

  navClassRules: [
    {
      className: 'has-example-icon',
      hrefRegex: '(?:^|/)examples/index\\.html$|(?:^|/)examples/\\d{2}_',
      titleRegex: '^(Example (总览|Overview))$|^\\d{2}\\s',
      pathRegex: '/packages/(?!index\\.html)[^/]+\\.html$',
      currentPathRegex: '/examples/',
    },
    {
      className: 'has-faq-icon',
      hrefRegex: '(?:^|/)fci/faq\\.html$',
      titleRegex: '^FAQ$',
      currentPathRegex: '/fci/faq\\.html$',
    },
  ],

  // Font Awesome glyph shown in front of a page entry.
  navGlyphs: {
    '/about/overview.html': '',
    '/about/concepts.html': '',
    '/guide/control_modes.html': '',
    '/guide/robot_state.html': '',
    '/guide/kinematics.html': '',
    '/guide/inverse_uniqueness.html': '',
    '/about/versions.html': '',
    '/programming/network.html': '',
    '/cpp/overview.html': '',
    '/cpp/development.html': '',
    '/cpp/quick_start.html': '',
    '/python/overview.html': '',
    '/python/development.html': '',
    '/python/quick_start.html': '',
    '/fci/overview.html': '',
    '/fci/machines.html': '',
    '/fci/development.html': '',
    '/fci/realtime_network.html': '',
    '/fci/control_modes.html': '',
    '/fci/quick_start.html': '',
    '/fci/faq.html': '',
    '/ros2/overview.html': '',
    '/ros2/humble/development.html': '',
    '/ros2/humble/quick_start.html': '',
    '/ros2/humble/packages/index.html': '',
    '/ros2/jazzy/development.html': '',
    '/ros2/jazzy/quick_start.html': '',
    '/ros2/jazzy/packages/index.html': '',
    '/reference/units.html': '',
    '/reference/safety.html': '',
    '/reference/io.html': '',
    '/reference/error_codes.html': '',
    '/reference/troubleshooting.html': '',
  },
};
