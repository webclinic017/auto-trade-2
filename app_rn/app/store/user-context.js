import React from 'react';
import {useAuth} from './auth-context';

const UserContext = React.createContext();

const UserProvider = props => (
  <UserContext.Provider value={useAuth().data.user} {...props} />
);

const useUser = () => React.useContext(UserContext);

export {UserProvider, useUser};
