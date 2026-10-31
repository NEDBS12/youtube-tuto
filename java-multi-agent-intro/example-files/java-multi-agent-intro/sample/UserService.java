import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

// Sample code to review (it has bugs on purpose)
public class UserService {

    private final Connection db;

    public UserService(Connection db) {
        this.db = db;
    }

    public boolean isAdmin(String username) throws SQLException {
        Statement st = db.createStatement();
        ResultSet rs = st.executeQuery(
            "SELECT role FROM users WHERE name = '" + username + "'");
        if (rs.next()) {
            return rs.getString("role") == "ADMIN";
        }
        return false;
    }
}
