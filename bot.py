    if text.startswith("رفع مشرف") and msg.reply_to_message:
        r = get_r(cid)
        # بس المطور Dev² و Dev يقدر يرفع
        if uid not in r["asasi"] and uid not in r["dev2"] and uid not in r["dev"] and msg.from_user.username != "ADJkex":
            if not await is_admin(update):
                await msg.reply_text("❌ بس Dev² 🎖️ و Dev 🎖️ يقدرون يرفعون مشرف من البوت")
                return
        
        try:
            await context.bot.promote_chat_member(
                cid, 
                msg.reply_to_message.from_user.id,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,      # ✅ يقدر يرفع
                can_manage_chat=True,          # ✅ يتحكم بالاعدادات
                can_manage_video_chats=True,   # ✅ يتحكم بالمكالمات
                is_anonymous=False
            )
            await msg.reply_text(f"✅ تم رفع {msg.reply_to_message.from_user.first_name} مشرف بكل الصلاحيات\nبواسطة المطور {msg.from_user.first_name}\n\n🔥 الحين يقدر يتحكم كامل")
        except Exception as e:
            await msg.reply_text(f"خطأ: {e}\nلازم البوت نفسه يكون مشرف بكل الصلاحيات")
        return
