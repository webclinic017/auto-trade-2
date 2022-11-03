import React from 'react';
import {View, Text} from 'react-native';
// import {FullPageSpinner} from '../components/lib';

const AuthContext = React.createContext();
const isLoading = false;

function AuthProvider(props) {
  if (isLoading) {
    // return <FullPageSpinner />;
    return (
      <View>
        <Text>Loading...</Text>
      </View>
    );
  }
  const data = {
    user: null,
  };
  const login = () => {}; // make a login request
  const register = () => {}; // register the user
  const logout = () => {}; // clear the token in localStorage and the user data

  // 注意：这里我并没有使用 `React.useMemo` 来优化 provider 的 `value`。
  // 因为这是我们应用里最顶级的组件，很少会在这个顶级组件上触发 重新render
  return (
    <AuthContext.Provider value={{data, login, logout, register}} {...props} />
  );
}

const useAuth = () => React.useContext(AuthContext);

export {AuthProvider, useAuth};

// user-context.js 文件里的 `UserProvider` 大概长这样：
// import React from 'react';
// import {useAuth} from './auth-context';

// const UserContext = React.createContext();

// const UserProvider = props => (
//   <UserContext.Provider value={useAuth().data.user} {...props} />
// );

// const useUser = () => React.useContext(UserContext);

// export {UserProvider, useUser};
