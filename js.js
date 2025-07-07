// netlify/functions/your-function.js
exports.handler = async (event) => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: "Success" }),
    headers: { 
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=3600"  // تخزين لمدة ساعة
    }
  };
};