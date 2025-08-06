# Codeforces User Comparison Tool

A desktop application that allows you to compare statistics between multiple Codeforces users side-by-side. Perfect for competitive programmers who want to analyze and compare their performance with friends, teammates, or rivals!

## Features

-  **Multi-User Comparison**: Compare up to 5 Codeforces users simultaneously
-  **Comprehensive Statistics**: View detailed metrics including:
   - Total problems solved and attempted
   - Average and maximum problem ratings
   - Top problem tags/categories
   - Programming languages used with frequency
-  **User-Friendly Interface**: Clean, modern GUI built with CustomTkinter
-  **Fast Performance**: Multi-threaded data fetching for quick results
-  **Grid Layout**: Easy-to-read comparison table format

## Screenshots

The application displays a comprehensive comparison grid showing all key metrics for each user, making it easy to spot differences in problem-solving patterns and skill levels.

## How to Use

1. **Launch the Application**: Run the executable or Python script
2. **Set Number of Users**: Enter how many Codeforces handles you want to compare (1-5)
3. **Enter Handles**: Input the Codeforces usernames in the generated fields
4. **Compare**: Click "Compare Stats" to fetch and display the comparison
5. **Analyze**: Review the side-by-side statistics in the results grid

### Keyboard Shortcuts
- Press `Enter` after entering the number of handles to generate input fields
- Press `Enter` in any handle field to move to the next field or start comparison
- Use the scroll wheel to navigate through results

## Statistics Explained

| Metric | Description |
|--------|-------------|
| **Total Solved** | Number of unique problems successfully solved |
| **Total Attempted** | Number of unique problems attempted (including unsolved) |
| **Average Problem Rating (solved)** | Average difficulty rating of solved problems |
| **Max Problem Rating (solved)** | Highest difficulty rating among solved problems |
| **Average Problem Rating (attempted)** | Average difficulty rating of all attempted problems |
| **Max Problem Rating (attempted)** | Highest difficulty rating among attempted problems |
| **Top Problem Tags** | Most frequently solved problem categories/topics |
| **Language Used** | Programming languages used with frequency count |

## Getting Started

To try the app, download the `CF_stat_comparator.exe` file - no installation required!

## Requirements

- **For Executable**: Windows OS (64-bit recommended)
- **For Source Code**: 
  - Python 3.7+
  - `customtkinter` library
  - `requests` library

## Technical Details

- **GUI Framework**: CustomTkinter for modern, themed interface
- **API**: Uses official Codeforces API for data retrieval
- **Threading**: Multi-threaded design prevents UI freezing during data fetch
- **Error Handling**: Graceful handling of invalid usernames and API errors

## Known Limitations

- Maximum of 5 users per comparison (to maintain readability)
- Requires active internet connection for API calls
- API rate limits may apply for very frequent requests
- Some problems may not have rating information available

## Troubleshooting

- **"Error for [username]"**: Check if the username exists and is spelled correctly
- **Slow loading**: Network issues or Codeforces API temporary unavailability
- **Application won't start**: Ensure you have proper permissions and Windows Defender isn't blocking the executable

## Contributing

Feel free to contribute by:
- Reporting bugs or issues
- Suggesting new features
- Submitting pull requests
- Improving documentation

## License

This project is open source. Please check the license file for more details.

## Download

Ready to compare your Codeforces stats? Download the latest version:

[![Download CF_Stat_Comparator.exe](https://img.shields.io/badge/Download-CF%20Stat%20Comparator-blue?style=for-the-badge&logo=download)](https://github.com/mi-shraban/CF_Stats_Comparator/releases/tag/v1.0.0)

**File**: `CF_stat_comparator.exe`  
**Size**: ~35MB  
**Platform**: Windows (64-bit recommended)

---
