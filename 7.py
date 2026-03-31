#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase_7.py
AI Chat Platform - Phase 7: Final Files & README
Landing page, database types, robots.txt, README, and all Shadcn/UI components.
"""

import os
import sys

def create_file(path: str, content: str) -> None:
    """Create a file with the given path and content, creating directories as needed."""
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ Created: {path}")

def main():
    print("=" * 60)
    print("🚀 AI Chat Platform - Phase 7: FINAL")
    print("   Landing Page + Database Types + UI Components + README")
    print("=" * 60)

    files_created = 0

    # =====================================================================
    # 1. LANDING PAGE
    # =====================================================================
    print("\n🏠 Landing Page")
    print("-" * 40)

    create_file("app/[locale]/page.tsx", '''// الصفحة الرئيسية - صفحة الهبوط للزوار غير المسجلين
// تعرض مميزات المنصة وأزرار تسجيل الدخول والتسجيل
// إذا كان المستخدم مسجل دخوله يتم توجيهه إلى /chat
import { redirect } from "next/navigation";
import { useTranslations } from "next-intl";
import { getTranslations } from "next-intl/server";
import Link from "next/link";
import type { Metadata } from "next";
import { createSupabaseServerClient } from "@/lib/supabase-server";

export async function generateMetadata({
  params: { locale },
}: {
  params: { locale: string };
}): Promise<Metadata> {
  const t = await getTranslations({ locale, namespace: "landing" });

  return {
    title: process.env.NEXT_PUBLIC_APP_NAME || "AI Chat Platform",
    description:
      locale === "ar"
        ? "منصة دردشة احترافية متعددة المنصات بالذكاء الاصطناعي مع شخصيات متخصصة"
        : "Professional Multi-Platform AI Chat Platform with Specialized Personas",
    openGraph: {
      title: process.env.NEXT_PUBLIC_APP_NAME || "AI Chat Platform",
      description:
        locale === "ar"
          ? "منصة دردشة احترافية متعددة المنصات بالذكاء الاصطناعي"
          : "Professional Multi-Platform AI Chat Platform",
      locale: locale === "ar" ? "ar_SA" : "en_US",
    },
  };
}

export default async function LandingPage({
  params: { locale },
}: {
  params: { locale: string };
}) {
  // التحقق من تسجيل الدخول - التوجيه إلى المحادثات
  try {
    const supabase = createSupabaseServerClient();
    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (session) {
      redirect(`/${locale}/chat`);
    }
  } catch {
    // متابعة عرض صفحة الهبوط
  }

  return <LandingContent locale={locale} />;
}

function LandingContent({ locale }: { locale: string }) {
  const isArabic = locale === "ar";

  const features = [
    {
      icon: "🌐",
      titleAr: "7 منصات ذكاء اصطناعي",
      titleEn: "7 AI Platforms",
      descAr:
        "تواصل مع OpenAI، Anthropic، Gemini، Groq، OpenRouter، Together AI، و Mistral من واجهة واحدة",
      descEn:
        "Connect with OpenAI, Anthropic, Gemini, Groq, OpenRouter, Together AI, and Mistral from one interface",
    },
    {
      icon: "🎭",
      titleAr: "شخصيات متخصصة",
      titleEn: "Specialized Personas",
      descAr:
        "استخدم شخصيات جاهزة مثل خبير LinkedIn وخبير العصف الذهني أو أنشئ شخصياتك المخصصة",
      descEn:
        "Use pre-built personas like LinkedIn Expert and Brainstorming Expert or create your own",
    },
    {
      icon: "🆓",
      titleAr: "مجاني للبدء",
      titleEn: "Free to Start",
      descAr:
        "ابدأ مجاناً مع مفاتيح API العامة أو أضف مفاتيحك الخاصة للاستخدام غير المحدود",
      descEn:
        "Start free with public API keys or add your own for unlimited usage",
    },
    {
      icon: "🌍",
      titleAr: "ثنائي اللغة",
      titleEn: "Bilingual",
      descAr:
        "واجهة كاملة بالعربية والإنجليزية مع دعم RTL/LTR التلقائي",
      descEn:
        "Full Arabic and English interface with automatic RTL/LTR support",
    },
    {
      icon: "📱",
      titleAr: "يعمل على جميع الأجهزة",
      titleEn: "Works on All Devices",
      descAr:
        "تصميم متجاوب يعمل بسلاسة على الهاتف والتابلت والكمبيوتر",
      descEn:
        "Responsive design that works seamlessly on mobile, tablet, and desktop",
    },
    {
      icon: "🔒",
      titleAr: "آمن ومشفّر",
      titleEn: "Secure & Encrypted",
      descAr:
        "جميع مفاتيح API مشفرة بتقنية AES-256 مع سياسات أمان صارمة",
      descEn:
        "All API keys encrypted with AES-256 and strict security policies",
    },
  ];

  return (
    <div className="min-h-screen bg-dark-900 text-white overflow-hidden">
      {/* الخلفية المتحركة */}
      <div className="fixed inset-0 z-0">
        <div className="absolute top-1/4 start-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-pulse-soft" />
        <div className="absolute bottom-1/4 end-1/4 w-96 h-96 bg-secondary/10 rounded-full blur-3xl animate-pulse-soft delay-1000" />
        <div className="absolute top-1/2 start-1/2 w-64 h-64 bg-accent/5 rounded-full blur-3xl animate-pulse-soft delay-500" />
      </div>

      {/* المحتوى الرئيسي */}
      <div className="relative z-10">
        {/* الشريط العلوي */}
        <header className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-xl font-bold">
              AI
            </div>
            <span className="text-xl font-bold text-gradient">
              {process.env.NEXT_PUBLIC_APP_NAME || "AI Chat Platform"}
            </span>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href={`/${locale === "ar" ? "en" : "ar"}`}
              className="px-3 py-1.5 text-sm rounded-lg border border-dark-500 text-dark-200 hover:bg-dark-700 transition-colors"
              aria-label={isArabic ? "Switch to English" : "التبديل للعربية"}
            >
              {isArabic ? "EN" : "عربي"}
            </Link>
            <Link
              href={`/${locale}/login`}
              className="px-4 py-2 text-sm rounded-lg border border-primary/50 text-primary hover:bg-primary/10 transition-colors"
            >
              {isArabic ? "تسجيل الدخول" : "Sign In"}
            </Link>
            <Link
              href={`/${locale}/register`}
              className="px-4 py-2 text-sm rounded-lg bg-primary hover:bg-primary-600 text-white transition-colors"
            >
              {isArabic ? "إنشاء حساب" : "Get Started"}
            </Link>
          </div>
        </header>

        {/* القسم الرئيسي (Hero) */}
        <section className="px-6 pt-16 pb-20 max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-sm mb-8">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
            {isArabic ? "مدعوم بأحدث نماذج الذكاء الاصطناعي" : "Powered by latest AI models"}
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight mb-6">
            {isArabic ? (
              <>
                <span className="text-gradient">دردش مع الذكاء الاصطناعي</span>
                <br />
                <span className="text-white">بطريقة احترافية</span>
              </>
            ) : (
              <>
                <span className="text-gradient">Chat with AI</span>
                <br />
                <span className="text-white">Like a Professional</span>
              </>
            )}
          </h1>

          <p className="text-lg sm:text-xl text-dark-300 max-w-2xl mx-auto mb-10 leading-relaxed">
            {isArabic
              ? "منصة موحدة للتواصل مع 7 منصات ذكاء اصطناعي عبر شخصيات متخصصة. اكتب محتوى احترافي، ولّد أفكاراً إبداعية، وحسّن إنتاجيتك."
              : "A unified platform to chat with 7 AI platforms through specialized personas. Write professional content, generate creative ideas, and boost your productivity."}
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href={`/${locale}/register`}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-primary to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold text-lg transition-all hover:shadow-lg hover:shadow-primary/25"
            >
              {isArabic ? "ابدأ مجاناً" : "Start for Free"}
            </Link>
            <Link
              href={`/${locale}/login`}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl border border-dark-500 text-dark-200 hover:bg-dark-700 font-semibold text-lg transition-colors"
            >
              {isArabic ? "تسجيل الدخول" : "Sign In"}
            </Link>
          </div>

          {/* شارات المنصات */}
          <div className="flex flex-wrap items-center justify-center gap-3 mt-12">
            {[
              { emoji: "🤖", name: "OpenAI" },
              { emoji: "🧠", name: "Anthropic" },
              { emoji: "💎", name: "Gemini" },
              { emoji: "⚡", name: "Groq" },
              { emoji: "🌐", name: "OpenRouter" },
              { emoji: "🤝", name: "Together" },
              { emoji: "🌀", name: "Mistral" },
            ].map((platform) => (
              <span
                key={platform.name}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-dark-700/50 border border-dark-600 text-sm text-dark-200"
              >
                <span>{platform.emoji}</span>
                {platform.name}
              </span>
            ))}
          </div>
        </section>

        {/* قسم المميزات */}
        <section className="px-6 py-20 max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">
            {isArabic ? "لماذا تختار منصتنا؟" : "Why Choose Our Platform?"}
          </h2>
          <p className="text-dark-300 text-center mb-12 max-w-xl mx-auto">
            {isArabic
              ? "مميزات متقدمة تجعل تجربتك مع الذكاء الاصطناعي فريدة"
              : "Advanced features that make your AI experience unique"}
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group p-6 rounded-2xl bg-dark-800/50 border border-dark-600 hover:border-primary/30 transition-all duration-300 hover:shadow-lg hover:shadow-primary/5"
              >
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold mb-2">
                  {isArabic ? feature.titleAr : feature.titleEn}
                </h3>
                <p className="text-dark-300 text-sm leading-relaxed">
                  {isArabic ? feature.descAr : feature.descEn}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* قسم الشخصيات */}
        <section className="px-6 py-20 max-w-5xl mx-auto">
          <div className="rounded-3xl bg-gradient-to-br from-primary/10 to-secondary/10 border border-primary/20 p-8 sm:p-12 text-center">
            <h2 className="text-3xl font-bold mb-4">
              {isArabic ? "شخصيات جاهزة للاستخدام" : "Ready-to-Use Personas"}
            </h2>
            <p className="text-dark-300 mb-8 max-w-lg mx-auto">
              {isArabic
                ? "ابدأ فوراً مع شخصيات متخصصة مُعدّة بعناية لتحقيق أفضل النتائج"
                : "Start immediately with carefully crafted specialized personas for best results"}
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-2xl mx-auto">
              {[
                { emoji: "💼", nameAr: "خبير LinkedIn", nameEn: "LinkedIn Expert", command: "/linkedin" },
                { emoji: "💡", nameAr: "عصف ذهني", nameEn: "Brainstorming", command: "/brainstorm" },
                { emoji: "🎯", nameAr: "هندسة برومبت", nameEn: "Prompt Engineering", command: "/prompt" },
                { emoji: "📧", nameAr: "كتابة بريد", nameEn: "Email Writing", command: "/email" },
              ].map((persona) => (
                <div
                  key={persona.command}
                  className="p-4 rounded-xl bg-dark-800/50 border border-dark-600"
                >
                  <span className="text-3xl mb-2 block">{persona.emoji}</span>
                  <p className="font-semibold text-sm mb-1">
                    {isArabic ? persona.nameAr : persona.nameEn}
                  </p>
                  <code className="text-xs text-primary">{persona.command}</code>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* قسم الدعوة للعمل (CTA) */}
        <section className="px-6 py-20 max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">
            {isArabic ? "مستعد للبدء؟" : "Ready to Start?"}
          </h2>
          <p className="text-dark-300 mb-8">
            {isArabic
              ? "أنشئ حسابك مجاناً الآن وابدأ المحادثة مع أقوى نماذج الذكاء الاصطناعي"
              : "Create your free account now and start chatting with the most powerful AI models"}
          </p>
          <Link
            href={`/${locale}/register`}
            className="inline-flex px-8 py-3.5 rounded-xl bg-gradient-to-r from-primary to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold text-lg transition-all hover:shadow-lg hover:shadow-primary/25"
          >
            {isArabic ? "إنشاء حساب مجاني" : "Create Free Account"}
          </Link>
        </section>

        {/* الذيل */}
        <footer className="px-6 py-8 border-t border-dark-700 text-center text-dark-400 text-sm">
          <p>
            © {new Date().getFullYear()}{" "}
            {process.env.NEXT_PUBLIC_APP_NAME || "AI Chat Platform"}.{" "}
            {isArabic ? "جميع الحقوق محفوظة." : "All rights reserved."}
          </p>
        </footer>
      </div>
    </div>
  );
}
''')
    files_created += 1

    # =====================================================================
    # 2. DATABASE TYPES
    # =====================================================================
    print("\n🗃️  Database Types")
    print("-" * 40)

    create_file("types/database.ts", '''// أنواع قاعدة البيانات الكاملة - تعريف TypeScript لجميع الجداول الـ 14
// يُستخدم مع عميل Supabase للحصول على أمان أنواع كامل

/**
 * تعريف قاعدة البيانات الكامل لـ Supabase
 * يشمل جميع الجداول مع أنواع Row و Insert و Update
 */
export interface Database {
  public: {
    Tables: {
      /** جدول الملفات الشخصية */
      profiles: {
        Row: {
          id: string;
          email: string;
          display_name: string | null;
          role: "admin" | "premium" | "free";
          is_super_admin: boolean;
          premium_expires_at: string | null;
          trial_used: boolean;
          trial_expires_at: string | null;
          is_banned: boolean;
          onboarding_completed: boolean;
          preferred_language: string;
          preferred_theme: string;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id: string;
          email: string;
          display_name?: string | null;
          role?: "admin" | "premium" | "free";
          is_super_admin?: boolean;
          premium_expires_at?: string | null;
          trial_used?: boolean;
          trial_expires_at?: string | null;
          is_banned?: boolean;
          onboarding_completed?: boolean;
          preferred_language?: string;
          preferred_theme?: string;
        };
        Update: {
          email?: string;
          display_name?: string | null;
          role?: "admin" | "premium" | "free";
          is_super_admin?: boolean;
          premium_expires_at?: string | null;
          trial_used?: boolean;
          trial_expires_at?: string | null;
          is_banned?: boolean;
          onboarding_completed?: boolean;
          preferred_language?: string;
          preferred_theme?: string;
          updated_at?: string;
        };
      };
      /** جدول المحادثات */
      conversations: {
        Row: {
          id: string;
          user_id: string;
          title: string;
          persona_id: string | null;
          platform: string;
          model: string;
          folder_id: string | null;
          is_favorited: boolean;
          message_count: number;
          total_tokens: number;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          title?: string;
          persona_id?: string | null;
          platform: string;
          model: string;
          folder_id?: string | null;
          is_favorited?: boolean;
          message_count?: number;
          total_tokens?: number;
        };
        Update: {
          user_id?: string;
          title?: string;
          persona_id?: string | null;
          platform?: string;
          model?: string;
          folder_id?: string | null;
          is_favorited?: boolean;
          message_count?: number;
          total_tokens?: number;
          updated_at?: string;
        };
      };
      /** جدول الرسائل */
      messages: {
        Row: {
          id: string;
          conversation_id: string;
          role: "user" | "assistant" | "system";
          content: string;
          model: string | null;
          platform: string | null;
          persona_name: string | null;
          tokens_used: number;
          response_time_ms: number | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          conversation_id: string;
          role: "user" | "assistant" | "system";
          content: string;
          model?: string | null;
          platform?: string | null;
          persona_name?: string | null;
          tokens_used?: number;
          response_time_ms?: number | null;
        };
        Update: {
          conversation_id?: string;
          role?: "user" | "assistant" | "system";
          content?: string;
          model?: string | null;
          platform?: string | null;
          persona_name?: string | null;
          tokens_used?: number;
          response_time_ms?: number | null;
        };
      };
      /** جدول الشخصيات */
      personas: {
        Row: {
          id: string;
          user_id: string | null;
          name: string;
          description: string;
          system_prompt: string;
          icon_url: string | null;
          category: string;
          type: "system" | "premium" | "custom" | "shared";
          is_active: boolean;
          is_approved: boolean;
          average_rating: number;
          rating_count: number;
          usage_count: number;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          user_id?: string | null;
          name: string;
          description: string;
          system_prompt: string;
          icon_url?: string | null;
          category: string;
          type: "system" | "premium" | "custom" | "shared";
          is_active?: boolean;
          is_approved?: boolean;
          average_rating?: number;
          rating_count?: number;
          usage_count?: number;
        };
        Update: {
          user_id?: string | null;
          name?: string;
          description?: string;
          system_prompt?: string;
          icon_url?: string | null;
          category?: string;
          type?: "system" | "premium" | "custom" | "shared";
          is_active?: boolean;
          is_approved?: boolean;
          average_rating?: number;
          rating_count?: number;
          usage_count?: number;
          updated_at?: string;
        };
      };
      /** جدول تقييمات الشخصيات */
      persona_ratings: {
        Row: {
          id: string;
          persona_id: string;
          user_id: string;
          rating: number;
          created_at: string;
        };
        Insert: {
          id?: string;
          persona_id: string;
          user_id: string;
          rating: number;
        };
        Update: {
          persona_id?: string;
          user_id?: string;
          rating?: number;
        };
      };
      /** جدول مفاتيح API */
      api_keys: {
        Row: {
          id: string;
          user_id: string | null;
          platform: string;
          encrypted_key: string;
          label: string;
          is_global: boolean;
          is_active: boolean;
          last_used_at: string | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          user_id?: string | null;
          platform: string;
          encrypted_key: string;
          label: string;
          is_global?: boolean;
          is_active?: boolean;
          last_used_at?: string | null;
        };
        Update: {
          user_id?: string | null;
          platform?: string;
          encrypted_key?: string;
          label?: string;
          is_global?: boolean;
          is_active?: boolean;
          last_used_at?: string | null;
        };
      };
      /** جدول النماذج العامة */
      global_models: {
        Row: {
          id: string;
          api_key_id: string;
          model_id: string;
          model_name: string;
          is_active: boolean;
          sort_order: number;
          created_at: string;
        };
        Insert: {
          id?: string;
          api_key_id: string;
          model_id: string;
          model_name: string;
          is_active?: boolean;
          sort_order?: number;
        };
        Update: {
          api_key_id?: string;
          model_id?: string;
          model_name?: string;
          is_active?: boolean;
          sort_order?: number;
        };
      };
      /** جدول المجلدات */
      folders: {
        Row: {
          id: string;
          user_id: string;
          name: string;
          type: "auto" | "custom";
          persona_id: string | null;
          sort_order: number;
          created_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          name: string;
          type: "auto" | "custom";
          persona_id?: string | null;
          sort_order?: number;
        };
        Update: {
          user_id?: string;
          name?: string;
          type?: "auto" | "custom";
          persona_id?: string | null;
          sort_order?: number;
        };
      };
      /** جدول أكواد الدعوة */
      invite_codes: {
        Row: {
          id: string;
          code: string;
          created_by: string;
          max_uses: number;
          current_uses: number;
          premium_duration_days: number | null;
          is_active: boolean;
          expires_at: string | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          code: string;
          created_by: string;
          max_uses?: number;
          current_uses?: number;
          premium_duration_days?: number | null;
          is_active?: boolean;
          expires_at?: string | null;
        };
        Update: {
          code?: string;
          created_by?: string;
          max_uses?: number;
          current_uses?: number;
          premium_duration_days?: number | null;
          is_active?: boolean;
          expires_at?: string | null;
        };
      };
      /** جدول استخدامات أكواد الدعوة */
      invite_code_uses: {
        Row: {
          id: string;
          invite_code_id: string;
          user_id: string;
          used_at: string;
        };
        Insert: {
          id?: string;
          invite_code_id: string;
          user_id: string;
        };
        Update: {
          invite_code_id?: string;
          user_id?: string;
          used_at?: string;
        };
      };
      /** جدول الإشعارات */
      notifications: {
        Row: {
          id: string;
          type: string;
          title: string;
          message: string;
          priority: "urgent" | "normal" | "info";
          is_read: boolean;
          related_user_id: string | null;
          metadata: Record<string, unknown> | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          type: string;
          title: string;
          message: string;
          priority?: "urgent" | "normal" | "info";
          is_read?: boolean;
          related_user_id?: string | null;
          metadata?: Record<string, unknown> | null;
        };
        Update: {
          type?: string;
          title?: string;
          message?: string;
          priority?: "urgent" | "normal" | "info";
          is_read?: boolean;
          related_user_id?: string | null;
          metadata?: Record<string, unknown> | null;
        };
      };
      /** جدول تجارب الشخصيات المميزة */
      premium_persona_trials: {
        Row: {
          id: string;
          user_id: string;
          persona_id: string;
          used_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          persona_id: string;
        };
        Update: {
          user_id?: string;
          persona_id?: string;
          used_at?: string;
        };
      };
      /** جدول المفضلات */
      user_favorites: {
        Row: {
          id: string;
          user_id: string;
          item_type: "persona" | "model";
          item_id: string;
          sort_order: number;
          created_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          item_type: "persona" | "model";
          item_id: string;
          sort_order?: number;
        };
        Update: {
          user_id?: string;
          item_type?: "persona" | "model";
          item_id?: string;
          sort_order?: number;
        };
      };
      /** جدول إحصائيات الاستخدام */
      usage_stats: {
        Row: {
          id: string;
          user_id: string;
          date: string;
          messages_sent: number;
          tokens_used: number;
          conversations_created: number;
          persona_id_most_used: string | null;
        };
        Insert: {
          id?: string;
          user_id: string;
          date: string;
          messages_sent?: number;
          tokens_used?: number;
          conversations_created?: number;
          persona_id_most_used?: string | null;
        };
        Update: {
          user_id?: string;
          date?: string;
          messages_sent?: number;
          tokens_used?: number;
          conversations_created?: number;
          persona_id_most_used?: string | null;
        };
      };
    };
    Functions: {
      is_admin: {
        Args: Record<string, never>;
        Returns: boolean;
      };
      is_super_admin: {
        Args: Record<string, never>;
        Returns: boolean;
      };
      get_user_role: {
        Args: Record<string, never>;
        Returns: string;
      };
      check_premium_expiry: {
        Args: Record<string, never>;
        Returns: undefined;
      };
      check_trial_expiry: {
        Args: Record<string, never>;
        Returns: undefined;
      };
    };
  };
}

/** اختصار لنوع صف من جدول معين */
export type TableRow<T extends keyof Database["public"]["Tables"]> =
  Database["public"]["Tables"][T]["Row"];

/** اختصار لنوع إدراج في جدول معين */
export type TableInsert<T extends keyof Database["public"]["Tables"]> =
  Database["public"]["Tables"][T]["Insert"];

/** اختصار لنوع تحديث في جدول معين */
export type TableUpdate<T extends keyof Database["public"]["Tables"]> =
  Database["public"]["Tables"][T]["Update"];
''')
    files_created += 1

    # =====================================================================
    # 3. ROBOTS.TXT
    # =====================================================================
    print("\n🤖 robots.txt")
    print("-" * 40)

    create_file("public/robots.txt", '''# منصة الدردشة بالذكاء الاصطناعي - AI Chat Platform
# https://your-app.pages.dev

User-agent: *
Allow: /
Allow: /ar
Allow: /en
Disallow: /chat
Disallow: /admin
Disallow: /settings
Disallow: /personas/create
Disallow: /api/
Disallow: /_next/
Disallow: /ar/chat
Disallow: /en/chat
Disallow: /ar/admin
Disallow: /en/admin
Disallow: /ar/settings
Disallow: /en/settings

Sitemap: https://your-app.pages.dev/sitemap.xml
''')
    files_created += 1

    # =====================================================================
    # 4. README.md
    # =====================================================================
    print("\n📖 README.md")
    print("-" * 40)

    create_file("README.md", '''# 🤖 AI Chat Platform

Professional Multi-Platform AI Chat Platform with Personas — منصة دردشة احترافية متعددة المنصات بالذكاء الاصطناعي مع شخصيات متخصصة

## ✨ Features

- **7 AI Platforms**: OpenRouter, Groq, OpenAI, Anthropic, Google Gemini, Together AI, Mistral
- **Persona System**: 4 built-in personas + custom creation + community sharing
- **3 Account Types**: Admin, Premium, Free with role-based access
- **Bilingual**: Full Arabic (RTL) + English (LTR) support
- **Real-time Streaming**: SSE streaming with typing indicator
- **AES-256 Encryption**: All API keys encrypted at rest
- **Rate Limiting**: Smart per-role rate limiting
- **Admin Dashboard**: Full user/key/model/persona/notification management
- **Telegram Notifications**: 9 event types with instant alerts
- **PWA Ready**: Installable progressive web app
- **Dark/Light Theme**: System-aware theme switching
- **Export/Import**: JSON and PDF export
- **Invite Codes**: Premium access via invite codes
- **Onboarding Tour**: 6-step guided tour for new users

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router), TypeScript (strict), Tailwind CSS 3.x |
| UI | Shadcn/UI, Lucide Icons, class-variance-authority |
| State | Zustand 4.x with persist middleware |
| AI | Vercel AI SDK, SSE streaming |
| i18n | next-intl (Arabic + English) |
| Auth | Supabase Auth (email + password) |
| Database | Supabase PostgreSQL with Row Level Security |
| Hosting | Cloudflare Pages (frontend), Cloudflare Workers (proxy) |
| Notifications | Telegram Bot API |
| Rendering | react-markdown, rehype-highlight |
| Export | jsPDF, file-saver |

## 📋 Prerequisites

- **Node.js** >= 18.x
- **npm** >= 9.x or **pnpm**
- **Supabase** account (free tier works)
- **Cloudflare** account (free tier works)
- **Telegram Bot** (optional, for notifications)

## 🔐 Environment Variables

Create `.env.local` from `.env.example`:

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | `https://xxx.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon/public key | `eyJhbG...` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key (secret) | `eyJhbG...` |
| `ENCRYPTION_KEY` | 32-character AES-256 key | `my-32-character-encryption-key!` |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | `123456:ABC-DEF...` |
| `TELEGRAM_CHAT_ID` | Telegram chat/group ID | `-1001234567890` |
| `SUPER_ADMIN_EMAIL` | Super admin email (auto-promoted) | `admin@example.com` |
| `SUPER_ADMIN_PASSWORD` | Super admin password | `StrongPass123!` |
| `NEXT_PUBLIC_APP_NAME` | Application display name | `AI Chat Platform` |
| `NEXT_PUBLIC_APP_URL` | Application URL | `https://your-app.pages.dev` |

## 🗄️ Supabase Setup

### 1. Create Project
1. Go to [supabase.com](https://supabase.com) and create a new project
2. Note your project URL and keys from Settings > API

### 2. Run SQL Files
Execute these SQL files **in order** in the Supabase SQL Editor:

```sql
-- Step 1: Create all 14 tables
-- Run: supabase/schema.sql

-- Step 2: Enable RLS and create policies
-- Run: supabase/rls-policies.sql

-- Step 3: Create functions and triggers
-- Run: supabase/functions.sql

-- Step 4: Seed initial data (4 built-in personas)
-- Run: supabase/seed.sql
```

### 3. Configure Auth
1. Go to Authentication > Settings
2. **Disable** email confirmation (for development)
3. Set Site URL to your app URL

### 4. Set Super Admin Email
In Supabase SQL Editor, set the app setting:

```sql
ALTER DATABASE postgres SET app.settings.super_admin_email = \'your-admin@email.com\';
```

## 🚀 Local Development

```bash
# 1. Clone the repository
git clone https://github.com/your-repo/ai-chat-platform.git
cd ai-chat-platform

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env.local
# Edit .env.local with your values

# 4. Start development server
npm run dev

# 5. Open in browser
open http://localhost:3000
```

## 👤 First-Time Setup

1. Start the app and go to the registration page
2. **Register with the email set in `SUPER_ADMIN_EMAIL`**
3. This account will automatically be set as Super Admin
4. Go to `/admin` to access the admin dashboard
5. Add global API keys for the platforms you want to support
6. Add models for each API key
7. Your users can now chat using the public API

## ☁️ Cloudflare Deployment

### Pages (Frontend)

```bash
# Build for Cloudflare Pages
npm run pages:build

# Deploy to Cloudflare Pages
npm run pages:deploy
```

Or connect your Git repository to Cloudflare Pages:
1. Go to Cloudflare Dashboard > Pages
2. Create a project from your Git repo
3. Build command: `npx @cloudflare/next-on-pages`
4. Output directory: `.vercel/output/static`
5. Add all environment variables

### Workers (AI Proxy)

```bash
# Deploy the AI proxy worker
cd workers
npx wrangler deploy

# Set secrets
npx wrangler secret put ENCRYPTION_KEY
npx wrangler secret put SUPABASE_SERVICE_ROLE_KEY
```

## 📁 Project Structure

```
ai-chat-platform/
├── app/                      # Next.js App Router
│   ├── [locale]/             # Locale-based routing (ar/en)
│   │   ├── layout.tsx        # Root layout with fonts and i18n
│   │   ├── page.tsx          # Landing page
│   │   ├── login/            # Login page
│   │   ├── register/         # Registration page
│   │   ├── chat/             # Chat interface
│   │   ├── personas/         # Personas library
│   │   ├── settings/         # User settings
│   │   └── admin/            # Admin dashboard
│   └── api/                  # API routes
│       ├── chat/             # AI chat endpoint
│       ├── models/           # Models endpoint
│       ├── auth/             # Auth callback
│       ├── admin/            # Admin endpoints
│       └── webhook/          # Telegram webhook
├── components/               # React components
│   ├── ui/                   # Shadcn/UI components
│   ├── chat/                 # Chat components
│   ├── sidebar/              # Sidebar components
│   ├── header/               # Header components
│   ├── personas/             # Persona components
│   ├── settings/             # Settings components
│   ├── admin/                # Admin components
│   ├── onboarding/           # Onboarding tour
│   ├── common/               # Common components
│   └── auth/                 # Auth components
├── lib/                      # Libraries
│   ├── supabase-client.ts    # Browser Supabase client
│   ├── supabase-server.ts    # Server Supabase client
│   ├── supabase-admin.ts     # Admin Supabase client
│   ├── ai-providers/         # AI platform adapters
│   ├── encryption.ts         # AES-256 encryption
│   ├── rate-limiter.ts       # Rate limiting logic
│   ├── telegram.ts           # Telegram notifications
│   └── export.ts             # Export utilities
├── hooks/                    # Custom React hooks
├── stores/                   # Zustand state stores
├── types/                    # TypeScript type definitions
├── utils/                    # Utility functions
├── i18n/                     # Translations (ar.json, en.json)
├── workers/                  # Cloudflare Workers
├── supabase/                 # Database schema and migrations
└── public/                   # Static assets
```

## 🔧 Troubleshooting

### Common Issues

**"Missing Supabase environment variables"**
- Ensure `.env.local` has `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Restart the dev server after changing env vars

**"RLS policy violation"**
- Run `supabase/rls-policies.sql` in Supabase SQL Editor
- Ensure the user is authenticated before making requests

**"Super admin not created"**
- Run the `ALTER DATABASE` command to set `app.settings.super_admin_email`
- Register with the exact email specified
- Check `supabase/functions.sql` was executed (the `handle_new_user` trigger)

**"API key encryption error"**
- Ensure `ENCRYPTION_KEY` is exactly 32 characters
- Use the same key across all environments

**"Models not loading"**
- Admin must add global API keys first
- Then add models linked to those API keys
- Check the API key is valid and active

**"Telegram notifications not working"**
- Create a bot via @BotFather on Telegram
- Get the chat ID by sending a message to the bot and checking the API
- Ensure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set

**"RTL layout issues"**
- The app uses `dir="rtl"` for Arabic and `dir="ltr"` for English
- Use `start`/`end` instead of `left`/`right` in Tailwind (e.g., `ps-4` not `pl-4`)

### Performance Tips

- Use private API keys for faster responses (no proxy delay)
- Premium users have a hidden 1-minute delay; free users have 3-minute visible delay
- The message limit per chat is 15 — start new conversations for long discussions

## 📄 License

This project is proprietary. All rights reserved.

---

Built with ❤️ using Next.js, Supabase, and Cloudflare
''')
    files_created += 1

    # =====================================================================
    # 5. SHADCN/UI COMPONENTS
    # =====================================================================
    print("\n🎨 Shadcn/UI Components")
    print("-" * 40)

    # button.tsx
    create_file("components/ui/button.tsx", '''// مكون الزر - Shadcn/UI مع متغيرات وأحجام متعددة
import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/utils/cn";

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-lg text-sm font-medium ring-offset-dark-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-white hover:bg-primary-600",
        destructive:
          "bg-red-600 text-white hover:bg-red-700",
        outline:
          "border border-dark-500 bg-transparent hover:bg-dark-700 text-dark-100",
        secondary:
          "bg-dark-600 text-white hover:bg-dark-500",
        ghost: "hover:bg-dark-700 text-dark-200 hover:text-white",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-lg px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
''')
    files_created += 1

    # input.tsx
    create_file("components/ui/input.tsx", '''// مكون حقل الإدخال - Shadcn/UI
import * as React from "react";
import { cn } from "@/utils/cn";

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-lg border border-dark-500 bg-dark-800 px-3 py-2 text-sm text-white ring-offset-dark-900 file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-dark-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);
Input.displayName = "Input";

export { Input };
''')
    files_created += 1

    # textarea.tsx
    create_file("components/ui/textarea.tsx", '''// مكون حقل النص المتعدد الأسطر - Shadcn/UI
import * as React from "react";
import { cn } from "@/utils/cn";

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "flex min-h-[80px] w-full rounded-lg border border-dark-500 bg-dark-800 px-3 py-2 text-sm text-white ring-offset-dark-900 placeholder:text-dark-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none",
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);
Textarea.displayName = "Textarea";

export { Textarea };
''')
    files_created += 1

    # label.tsx
    create_file("components/ui/label.tsx", '''// مكون التسمية - Shadcn/UI
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/utils/cn";

const labelVariants = cva(
  "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-dark-100"
);

export interface LabelProps
  extends React.LabelHTMLAttributes<HTMLLabelElement>,
    VariantProps<typeof labelVariants> {}

const Label = React.forwardRef<HTMLLabelElement, LabelProps>(
  ({ className, ...props }, ref) => {
    return (
      <label
        ref={ref}
        className={cn(labelVariants(), className)}
        {...props}
      />
    );
  }
);
Label.displayName = "Label";

export { Label };
''')
    files_created += 1

    # badge.tsx
    create_file("components/ui/badge.tsx", '''// مكون الشارة - Shadcn/UI مع متغيرات ألوان
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/utils/cn";

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-primary text-white",
        secondary:
          "border-transparent bg-dark-600 text-dark-100",
        destructive:
          "border-transparent bg-red-600 text-white",
        outline: "text-dark-200 border-dark-500",
        success:
          "border-transparent bg-green-600 text-white",
        warning:
          "border-transparent bg-yellow-600 text-white",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
''')
    files_created += 1

    # card.tsx
    create_file("components/ui/card.tsx", '''// مكون البطاقة - Shadcn/UI
import * as React from "react";
import { cn } from "@/utils/cn";

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-xl border border-dark-600 bg-dark-800 text-white shadow-sm",
      className
    )}
    {...props}
  />
));
Card.displayName = "Card";

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
));
CardHeader.displayName = "CardHeader";

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-xl font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  />
));
CardTitle.displayName = "CardTitle";

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-dark-300", className)}
    {...props}
  />
));
CardDescription.displayName = "CardDescription";

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
));
CardContent.displayName = "CardContent";

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
));
CardFooter.displayName = "CardFooter";

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };
''')
    files_created += 1

    # skeleton.tsx
    create_file("components/ui/skeleton.tsx", '''// مكون الهيكل العظمي للتحميل - Shadcn/UI
import { cn } from "@/utils/cn";

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-dark-600", className)}
      {...props}
    />
  );
}

export { Skeleton };
''')
    files_created += 1

    # separator.tsx
    create_file("components/ui/separator.tsx", '''// مكون الفاصل - Shadcn/UI
"use client";

import * as React from "react";
import * as SeparatorPrimitive from "@radix-ui/react-separator";
import { cn } from "@/utils/cn";

const Separator = React.forwardRef<
  React.ElementRef<typeof SeparatorPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof SeparatorPrimitive.Root>
>(
  (
    { className, orientation = "horizontal", decorative = true, ...props },
    ref
  ) => (
    <SeparatorPrimitive.Root
      ref={ref}
      decorative={decorative}
      orientation={orientation}
      className={cn(
        "shrink-0 bg-dark-600",
        orientation === "horizontal" ? "h-[1px] w-full" : "h-full w-[1px]",
        className
      )}
      {...props}
    />
  )
);
Separator.displayName = SeparatorPrimitive.Root.displayName;

export { Separator };
''')
    files_created += 1

    # avatar.tsx
    create_file("components/ui/avatar.tsx", '''// مكون الصورة الرمزية - Shadcn/UI
"use client";

import * as React from "react";
import * as AvatarPrimitive from "@radix-ui/react-avatar";
import { cn } from "@/utils/cn";

const Avatar = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Root
    ref={ref}
    className={cn(
      "relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full",
      className
    )}
    {...props}
  />
));
Avatar.displayName = AvatarPrimitive.Root.displayName;

const AvatarImage = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Image>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Image>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Image
    ref={ref}
    className={cn("aspect-square h-full w-full", className)}
    {...props}
  />
));
AvatarImage.displayName = AvatarPrimitive.Image.displayName;

const AvatarFallback = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Fallback>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Fallback>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Fallback
    ref={ref}
    className={cn(
      "flex h-full w-full items-center justify-center rounded-full bg-dark-600 text-dark-200 text-sm font-medium",
      className
    )}
    {...props}
  />
));
AvatarFallback.displayName = AvatarPrimitive.Fallback.displayName;

export { Avatar, AvatarImage, AvatarFallback };
''')
    files_created += 1

    # dialog.tsx
    create_file("components/ui/dialog.tsx", '''// مكون الحوار المنبثق - Shadcn/UI
"use client";

import * as React from "react";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import { cn } from "@/utils/cn";

const Dialog = DialogPrimitive.Root;
const DialogTrigger = DialogPrimitive.Trigger;
const DialogClose = DialogPrimitive.Close;
const DialogPortal = DialogPrimitive.Portal;

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 bg-black/60 backdrop-blur-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
  />
));
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName;

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border border-dark-600 bg-dark-800 p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] rounded-xl",
        className
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute end-4 top-4 rounded-sm opacity-70 ring-offset-dark-900 transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-dark-700">
        <X className="h-4 w-4 text-dark-300" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
));
DialogContent.displayName = DialogPrimitive.Content.displayName;

const DialogHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-col space-y-1.5 text-center sm:text-start",
      className
    )}
    {...props}
  />
);
DialogHeader.displayName = "DialogHeader";

const DialogFooter = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2 gap-2",
      className
    )}
    {...props}
  />
);
DialogFooter.displayName = "DialogFooter";

const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn(
      "text-lg font-semibold leading-none tracking-tight text-white",
      className
    )}
    {...props}
  />
));
DialogTitle.displayName = DialogPrimitive.Title.displayName;

const DialogDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-dark-300", className)}
    {...props}
  />
));
DialogDescription.displayName = DialogPrimitive.Description.displayName;

export {
  Dialog,
  DialogPortal,
  DialogOverlay,
  DialogClose,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
};
''')
    files_created += 1

    # dropdown-menu.tsx
    create_file("components/ui/dropdown-menu.tsx", '''// مكون القائمة المنسدلة - Shadcn/UI
"use client";

import * as React from "react";
import * as DropdownMenuPrimitive from "@radix-ui/react-dropdown-menu";
import { Check, ChevronRight, Circle } from "lucide-react";
import { cn } from "@/utils/cn";

const DropdownMenu = DropdownMenuPrimitive.Root;
const DropdownMenuTrigger = DropdownMenuPrimitive.Trigger;
const DropdownMenuGroup = DropdownMenuPrimitive.Group;
const DropdownMenuPortal = DropdownMenuPrimitive.Portal;
const DropdownMenuSub = DropdownMenuPrimitive.Sub;
const DropdownMenuRadioGroup = DropdownMenuPrimitive.RadioGroup;

const DropdownMenuSubTrigger = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.SubTrigger>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.SubTrigger> & {
    inset?: boolean;
  }
>(({ className, inset, children, ...props }, ref) => (
  <DropdownMenuPrimitive.SubTrigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-md px-2 py-1.5 text-sm outline-none focus:bg-dark-600 data-[state=open]:bg-dark-600 text-dark-100",
      inset && "ps-8",
      className
    )}
    {...props}
  >
    {children}
    <ChevronRight className="ms-auto h-4 w-4" />
  </DropdownMenuPrimitive.SubTrigger>
));
DropdownMenuSubTrigger.displayName =
  DropdownMenuPrimitive.SubTrigger.displayName;

const DropdownMenuSubContent = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.SubContent>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.SubContent>
>(({ className, ...props }, ref) => (
  <DropdownMenuPrimitive.SubContent
    ref={ref}
    className={cn(
      "z-50 min-w-[8rem] overflow-hidden rounded-xl border border-dark-600 bg-dark-800 p-1 text-dark-100 shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95",
      className
    )}
    {...props}
  />
));
DropdownMenuSubContent.displayName =
  DropdownMenuPrimitive.SubContent.displayName;

const DropdownMenuContent = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Content>
>(({ className, sideOffset = 4, ...props }, ref) => (
  <DropdownMenuPrimitive.Portal>
    <DropdownMenuPrimitive.Content
      ref={ref}
      sideOffset={sideOffset}
      className={cn(
        "z-50 min-w-[8rem] overflow-hidden rounded-xl border border-dark-600 bg-dark-800 p-1 text-dark-100 shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95",
        className
      )}
      {...props}
    />
  </DropdownMenuPrimitive.Portal>
));
DropdownMenuContent.displayName = DropdownMenuPrimitive.Content.displayName;

const DropdownMenuItem = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Item> & {
    inset?: boolean;
  }
>(({ className, inset, ...props }, ref) => (
  <DropdownMenuPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-pointer select-none items-center rounded-md px-2 py-1.5 text-sm outline-none transition-colors focus:bg-dark-600 focus:text-white data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      inset && "ps-8",
      className
    )}
    {...props}
  />
));
DropdownMenuItem.displayName = DropdownMenuPrimitive.Item.displayName;

const DropdownMenuCheckboxItem = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.CheckboxItem>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.CheckboxItem>
>(({ className, children, checked, ...props }, ref) => (
  <DropdownMenuPrimitive.CheckboxItem
    ref={ref}
    className={cn(
      "relative flex cursor-pointer select-none items-center rounded-md py-1.5 ps-8 pe-2 text-sm outline-none transition-colors focus:bg-dark-600 focus:text-white data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    checked={checked}
    {...props}
  >
    <span className="absolute start-2 flex h-3.5 w-3.5 items-center justify-center">
      <DropdownMenuPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </DropdownMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </DropdownMenuPrimitive.CheckboxItem>
));
DropdownMenuCheckboxItem.displayName =
  DropdownMenuPrimitive.CheckboxItem.displayName;

const DropdownMenuRadioItem = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.RadioItem>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.RadioItem>
>(({ className, children, ...props }, ref) => (
  <DropdownMenuPrimitive.RadioItem
    ref={ref}
    className={cn(
      "relative flex cursor-pointer select-none items-center rounded-md py-1.5 ps-8 pe-2 text-sm outline-none transition-colors focus:bg-dark-600 focus:text-white data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    {...props}
  >
    <span className="absolute start-2 flex h-3.5 w-3.5 items-center justify-center">
      <DropdownMenuPrimitive.ItemIndicator>
        <Circle className="h-2 w-2 fill-current" />
      </DropdownMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </DropdownMenuPrimitive.RadioItem>
));
DropdownMenuRadioItem.displayName =
  DropdownMenuPrimitive.RadioItem.displayName;

const DropdownMenuLabel = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Label> & {
    inset?: boolean;
  }
>(({ className, inset, ...props }, ref) => (
  <DropdownMenuPrimitive.Label
    ref={ref}
    className={cn(
      "px-2 py-1.5 text-sm font-semibold text-white",
      inset && "ps-8",
      className
    )}
    {...props}
  />
));
DropdownMenuLabel.displayName = DropdownMenuPrimitive.Label.displayName;

const DropdownMenuSeparator = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <DropdownMenuPrimitive.Separator
    ref={ref}
    className={cn("-mx-1 my-1 h-px bg-dark-600", className)}
    {...props}
  />
));
DropdownMenuSeparator.displayName =
  DropdownMenuPrimitive.Separator.displayName;

const DropdownMenuShortcut = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLSpanElement>) => {
  return (
    <span
      className={cn("ms-auto text-xs tracking-widest text-dark-400", className)}
      {...props}
    />
  );
};
DropdownMenuShortcut.displayName = "DropdownMenuShortcut";

export {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuCheckboxItem,
  DropdownMenuRadioItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuGroup,
  DropdownMenuPortal,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuRadioGroup,
};
''')
    files_created += 1

    # select.tsx
    create_file("components/ui/select.tsx", '''// مكون القائمة المنسدلة للاختيار - Shadcn/UI
"use client";

import * as React from "react";
import * as SelectPrimitive from "@radix-ui/react-select";
import { Check, ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "@/utils/cn";

const Select = SelectPrimitive.Root;
const SelectGroup = SelectPrimitive.Group;
const SelectValue = SelectPrimitive.Value;

const SelectTrigger = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Trigger
    ref={ref}
    className={cn(
      "flex h-10 w-full items-center justify-between rounded-lg border border-dark-500 bg-dark-800 px-3 py-2 text-sm text-white ring-offset-dark-900 placeholder:text-dark-400 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1",
      className
    )}
    {...props}
  >
    {children}
    <SelectPrimitive.Icon asChild>
      <ChevronDown className="h-4 w-4 opacity-50" />
    </SelectPrimitive.Icon>
  </SelectPrimitive.Trigger>
));
SelectTrigger.displayName = SelectPrimitive.Trigger.displayName;

const SelectScrollUpButton = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.ScrollUpButton>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollUpButton>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollUpButton
    ref={ref}
    className={cn(
      "flex cursor-default items-center justify-center py-1",
      className
    )}
    {...props}
  >
    <ChevronUp className="h-4 w-4" />
  </SelectPrimitive.ScrollUpButton>
));
SelectScrollUpButton.displayName =
  SelectPrimitive.ScrollUpButton.displayName;

const SelectScrollDownButton = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.ScrollDownButton>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollDownButton>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollDownButton
    ref={ref}
    className={cn(
      "flex cursor-default items-center justify-center py-1",
      className
    )}
    {...props}
  >
    <ChevronDown className="h-4 w-4" />
  </SelectPrimitive.ScrollDownButton>
));
SelectScrollDownButton.displayName =
  SelectPrimitive.ScrollDownButton.displayName;

const SelectContent = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Content>
>(({ className, children, position = "popper", ...props }, ref) => (
  <SelectPrimitive.Portal>
    <SelectPrimitive.Content
      ref={ref}
      className={cn(
        "relative z-50 max-h-96 min-w-[8rem] overflow-hidden rounded-xl border border-dark-600 bg-dark-800 text-dark-100 shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95",
        position === "popper" &&
          "data-[side=bottom]:translate-y-1 data-[side=left]:translate-x-[-1] data-[side=right]:translate-x-1 data-[side=top]:translate-y-[-1]",
        className
      )}
      position={position}
      {...props}
    >
      <SelectScrollUpButton />
      <SelectPrimitive.Viewport
        className={cn(
          "p-1",
          position === "popper" &&
            "h-[var(--radix-select-trigger-height)] w-full min-w-[var(--radix-select-trigger-width)]"
        )}
      >
        {children}
      </SelectPrimitive.Viewport>
      <SelectScrollDownButton />
    </SelectPrimitive.Content>
  </SelectPrimitive.Portal>
));
SelectContent.displayName = SelectPrimitive.Content.displayName;

const SelectLabel = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Label>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Label
    ref={ref}
    className={cn("py-1.5 ps-8 pe-2 text-sm font-semibold text-white", className)}
    {...props}
  />
));
SelectLabel.displayName = SelectPrimitive.Label.displayName;

const SelectItem = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Item>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex w-full cursor-pointer select-none items-center rounded-md py-1.5 ps-8 pe-2 text-sm outline-none focus:bg-dark-600 focus:text-white data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    {...props}
  >
    <span className="absolute start-2 flex h-3.5 w-3.5 items-center justify-center">
      <SelectPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </SelectPrimitive.ItemIndicator>
    </span>
    <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
  </SelectPrimitive.Item>
));
SelectItem.displayName = SelectPrimitive.Item.displayName;

const SelectSeparator = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Separator
    ref={ref}
    className={cn("-mx-1 my-1 h-px bg-dark-600", className)}
    {...props}
  />
));
SelectSeparator.displayName = SelectPrimitive.Separator.displayName;

export {
  Select,
  SelectGroup,
  SelectValue,
  SelectTrigger,
  SelectContent,
  SelectLabel,
  SelectItem,
  SelectSeparator,
  SelectScrollUpButton,
  SelectScrollDownButton,
};
''')
    files_created += 1

    # tabs.tsx
    create_file("components/ui/tabs.tsx", '''// مكون التبويبات - Shadcn/UI
"use client";

import * as React from "react";
import * as TabsPrimitive from "@radix-ui/react-tabs";
import { cn } from "@/utils/cn";

const Tabs = TabsPrimitive.Root;

const TabsList = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.List>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      "inline-flex h-10 items-center justify-center rounded-lg bg-dark-700 p-1 text-dark-300",
      className
    )}
    {...props}
  />
));
TabsList.displayName = TabsPrimitive.List.displayName;

const TabsTrigger = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Trigger
    ref={ref}
    className={cn(
      "inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1.5 text-sm font-medium ring-offset-dark-900 transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-dark-800 data-[state=active]:text-white data-[state=active]:shadow-sm",
      className
    )}
    {...props}
  />
));
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName;

const TabsContent = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      "mt-2 ring-offset-dark-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2",
      className
    )}
    {...props}
  />
));
TabsContent.displayName = TabsPrimitive.Content.displayName;

export { Tabs, TabsList, TabsTrigger, TabsContent };
''')
    files_created += 1

    # tooltip.tsx
    create_file("components/ui/tooltip.tsx", '''// مكون التلميحات - Shadcn/UI
"use client";

import * as React from "react";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import { cn } from "@/utils/cn";

const TooltipProvider = TooltipPrimitive.Provider;

const Tooltip = TooltipPrimitive.Root;

const TooltipTrigger = TooltipPrimitive.Trigger;

const TooltipContent = React.forwardRef<
  React.ElementRef<typeof TooltipPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Content>
>(({ className, sideOffset = 4, ...props }, ref) => (
  <TooltipPrimitive.Content
    ref={ref}
    sideOffset={sideOffset}
    className={cn(
      "z-50 overflow-hidden rounded-lg border border-dark-600 bg-dark-700 px-3 py-1.5 text-sm text-dark-100 shadow-md animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95",
      className
    )}
    {...props}
  />
));
TooltipContent.displayName = TooltipPrimitive.Content.displayName;

export { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider };
''')
    files_created += 1

    # switch.tsx
    create_file("components/ui/switch.tsx", '''// مكون مفتاح التبديل - Shadcn/UI
"use client";

import * as React from "react";
import * as SwitchPrimitives from "@radix-ui/react-switch";
import { cn } from "@/utils/cn";

const Switch = React.forwardRef<
  React.ElementRef<typeof SwitchPrimitives.Root>,
  React.ComponentPropsWithoutRef<typeof SwitchPrimitives.Root>
>(({ className, ...props }, ref) => (
  <SwitchPrimitives.Root
    className={cn(
      "peer inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-dark-900 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=unchecked]:bg-dark-500",
      className
    )}
    {...props}
    ref={ref}
  >
    <SwitchPrimitives.Thumb
      className={cn(
        "pointer-events-none block h-5 w-5 rounded-full bg-white shadow-lg ring-0 transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0 rtl:data-[state=checked]:-translate-x-5"
      )}
    />
  </SwitchPrimitives.Root>
));
Switch.displayName = SwitchPrimitives.Root.displayName;

export { Switch };
''')
    files_created += 1

    # scroll-area.tsx
    create_file("components/ui/scroll-area.tsx", '''// مكون منطقة التمرير - Shadcn/UI
"use client";

import * as React from "react";
import * as ScrollAreaPrimitive from "@radix-ui/react-scroll-area";
import { cn } from "@/utils/cn";

const ScrollArea = React.forwardRef<
  React.ElementRef<typeof ScrollAreaPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof ScrollAreaPrimitive.Root>
>(({ className, children, ...props }, ref) => (
  <ScrollAreaPrimitive.Root
    ref={ref}
    className={cn("relative overflow-hidden", className)}
    {...props}
  >
    <ScrollAreaPrimitive.Viewport className="h-full w-full rounded-[inherit]">
      {children}
    </ScrollAreaPrimitive.Viewport>
    <ScrollBar />
    <ScrollAreaPrimitive.Corner />
  </ScrollAreaPrimitive.Root>
));
ScrollArea.displayName = ScrollAreaPrimitive.Root.displayName;

const ScrollBar = React.forwardRef<
  React.ElementRef<typeof ScrollAreaPrimitive.ScrollAreaScrollbar>,
  React.ComponentPropsWithoutRef<typeof ScrollAreaPrimitive.ScrollAreaScrollbar>
>(({ className, orientation = "vertical", ...props }, ref) => (
  <ScrollAreaPrimitive.ScrollAreaScrollbar
    ref={ref}
    orientation={orientation}
    className={cn(
      "flex touch-none select-none transition-colors",
      orientation === "vertical" &&
        "h-full w-2.5 border-l border-l-transparent p-[1px]",
      orientation === "horizontal" &&
        "h-2.5 flex-col border-t border-t-transparent p-[1px]",
      className
    )}
    {...props}
  >
    <ScrollAreaPrimitive.ScrollAreaThumb className="relative flex-1 rounded-full bg-dark-500" />
  </ScrollAreaPrimitive.ScrollAreaScrollbar>
));
ScrollBar.displayName = ScrollAreaPrimitive.ScrollAreaScrollbar.displayName;

export { ScrollArea, ScrollBar };
''')
    files_created += 1

    # table.tsx
    create_file("components/ui/table.tsx", '''// مكون الجدول - Shadcn/UI
import * as React from "react";
import { cn } from "@/utils/cn";

const Table = React.forwardRef<
  HTMLTableElement,
  React.HTMLAttributes<HTMLTableElement>
>(({ className, ...props }, ref) => (
  <div className="relative w-full overflow-auto">
    <table
      ref={ref}
      className={cn("w-full caption-bottom text-sm", className)}
      {...props}
    />
  </div>
));
Table.displayName = "Table";

const TableHeader = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <thead ref={ref} className={cn("[&_tr]:border-b", className)} {...props} />
));
TableHeader.displayName = "TableHeader";

const TableBody = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <tbody
    ref={ref}
    className={cn("[&_tr:last-child]:border-0", className)}
    {...props}
  />
));
TableBody.displayName = "TableBody";

const TableFooter = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <tfoot
    ref={ref}
    className={cn(
      "border-t bg-dark-700/50 font-medium [&>tr]:last:border-b-0",
      className
    )}
    {...props}
  />
));
TableFooter.displayName = "TableFooter";

const TableRow = React.forwardRef<
  HTMLTableRowElement,
  React.HTMLAttributes<HTMLTableRowElement>
>(({ className, ...props }, ref) => (
  <tr
    ref={ref}
    className={cn(
      "border-b border-dark-600 transition-colors hover:bg-dark-700/50 data-[state=selected]:bg-dark-700",
      className
    )}
    {...props}
  />
));
TableRow.displayName = "TableRow";

const TableHead = React.forwardRef<
  HTMLTableCellElement,
  React.ThHTMLAttributes<HTMLTableCellElement>
>(({ className, ...props }, ref) => (
  <th
    ref={ref}
    className={cn(
      "h-12 px-4 text-start align-middle font-medium text-dark-300 [&:has([role=checkbox])]:pe-0",
      className
    )}
    {...props}
  />
));
TableHead.displayName = "TableHead";

const TableCell = React.forwardRef<
  HTMLTableCellElement,
  React.TdHTMLAttributes<HTMLTableCellElement>
>(({ className, ...props }, ref) => (
  <td
    ref={ref}
    className={cn(
      "p-4 align-middle text-dark-100 [&:has([role=checkbox])]:pe-0",
      className
    )}
    {...props}
  />
));
TableCell.displayName = "TableCell";

const TableCaption = React.forwardRef<
  HTMLTableCaptionElement,
  React.HTMLAttributes<HTMLTableCaptionElement>
>(({ className, ...props }, ref) => (
  <caption
    ref={ref}
    className={cn("mt-4 text-sm text-dark-400", className)}
    {...props}
  />
));
TableCaption.displayName = "TableCaption";

export {
  Table,
  TableHeader,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  TableCell,
  TableCaption,
};
''')
    files_created += 1

    # toast.tsx
    create_file("components/ui/toast.tsx", '''// مكون الإشعار المنبثق (Toast) - Shadcn/UI
"use client";

import * as React from "react";
import * as ToastPrimitives from "@radix-ui/react-toast";
import { cva, type VariantProps } from "class-variance-authority";
import { X } from "lucide-react";
import { cn } from "@/utils/cn";

const ToastProvider = ToastPrimitives.Provider;

const ToastViewport = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Viewport>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Viewport>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Viewport
    ref={ref}
    className={cn(
      "fixed top-0 z-[100] flex max-h-screen w-full flex-col-reverse p-4 sm:bottom-0 sm:end-0 sm:top-auto sm:flex-col md:max-w-[420px]",
      className
    )}
    {...props}
  />
));
ToastViewport.displayName = ToastPrimitives.Viewport.displayName;

const toastVariants = cva(
  "group pointer-events-auto relative flex w-full items-center justify-between space-x-4 overflow-hidden rounded-xl border p-6 pe-8 shadow-lg transition-all data-[swipe=cancel]:translate-x-0 data-[swipe=end]:translate-x-[var(--radix-toast-swipe-end-x)] data-[swipe=move]:translate-x-[var(--radix-toast-swipe-move-x)] data-[swipe=move]:transition-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[swipe=end]:animate-out data-[state=closed]:fade-out-80 data-[state=closed]:slide-out-to-right-full data-[state=open]:slide-in-from-top-full data-[state=open]:sm:slide-in-from-bottom-full",
  {
    variants: {
      variant: {
        default: "border-dark-600 bg-dark-800 text-white",
        destructive:
          "destructive group border-red-600 bg-red-600 text-white",
        success:
          "border-green-600 bg-green-600/10 text-green-400 border",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

const Toast = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Root>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Root> &
    VariantProps<typeof toastVariants>
>(({ className, variant, ...props }, ref) => {
  return (
    <ToastPrimitives.Root
      ref={ref}
      className={cn(toastVariants({ variant }), className)}
      {...props}
    />
  );
});
Toast.displayName = ToastPrimitives.Root.displayName;

const ToastAction = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Action>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Action>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Action
    ref={ref}
    className={cn(
      "inline-flex h-8 shrink-0 items-center justify-center rounded-md border border-dark-500 bg-transparent px-3 text-sm font-medium ring-offset-dark-900 transition-colors hover:bg-dark-700 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 group-[.destructive]:border-red-400/30 group-[.destructive]:hover:border-red-400/30 group-[.destructive]:hover:bg-red-600 group-[.destructive]:hover:text-white group-[.destructive]:focus:ring-red-400",
      className
    )}
    {...props}
  />
));
ToastAction.displayName = ToastPrimitives.Action.displayName;

const ToastClose = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Close>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Close>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Close
    ref={ref}
    className={cn(
      "absolute end-2 top-2 rounded-md p-1 text-dark-300 opacity-0 transition-opacity hover:text-white focus:opacity-100 focus:outline-none focus:ring-2 group-hover:opacity-100 group-[.destructive]:text-red-100 group-[.destructive]:hover:text-red-50",
      className
    )}
    toast-close=""
    {...props}
  >
    <X className="h-4 w-4" />
  </ToastPrimitives.Close>
));
ToastClose.displayName = ToastPrimitives.Close.displayName;

const ToastTitle = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Title>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Title>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Title
    ref={ref}
    className={cn("text-sm font-semibold", className)}
    {...props}
  />
));
ToastTitle.displayName = ToastPrimitives.Title.displayName;

const ToastDescription = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Description>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Description>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Description
    ref={ref}
    className={cn("text-sm opacity-90", className)}
    {...props}
  />
));
ToastDescription.displayName = ToastPrimitives.Description.displayName;

type ToastProps = React.ComponentPropsWithoutRef<typeof Toast>;
type ToastActionElement = React.ReactElement<typeof ToastAction>;

export {
  type ToastProps,
  type ToastActionElement,
  ToastProvider,
  ToastViewport,
  Toast,
  ToastTitle,
  ToastDescription,
  ToastClose,
  ToastAction,
};
''')
    files_created += 1

    # toaster.tsx
    create_file("components/ui/toaster.tsx", '''// مكون مزود الإشعارات المنبثقة - Shadcn/UI
"use client";

import {
  Toast,
  ToastClose,
  ToastDescription,
  ToastProvider,
  ToastTitle,
  ToastViewport,
} from "@/components/ui/toast";
import { useToast } from "@/hooks/useToast";

export function Toaster() {
  const { toasts } = useToast();

  return (
    <ToastProvider>
      {toasts.map(function ({ id, title, description, action, ...props }) {
        return (
          <Toast key={id} {...props}>
            <div className="grid gap-1">
              {title && <ToastTitle>{title}</ToastTitle>}
              {description && (
                <ToastDescription>{description}</ToastDescription>
              )}
            </div>
            {action}
            <ToastClose />
          </Toast>
        );
      })}
      <ToastViewport />
    </ToastProvider>
  );
}
''')
    files_created += 1

    # useToast hook (required by toaster)
    create_file("hooks/useToast.ts", '''// هوك الإشعارات المنبثقة - يدير حالة الإشعارات وعرضها
"use client";

import * as React from "react";
import type { ToastActionElement, ToastProps } from "@/components/ui/toast";

const TOAST_LIMIT = 5;
const TOAST_REMOVE_DELAY = 5000;

type ToasterToast = ToastProps & {
  id: string;
  title?: React.ReactNode;
  description?: React.ReactNode;
  action?: ToastActionElement;
};

const actionTypes = {
  ADD_TOAST: "ADD_TOAST",
  UPDATE_TOAST: "UPDATE_TOAST",
  DISMISS_TOAST: "DISMISS_TOAST",
  REMOVE_TOAST: "REMOVE_TOAST",
} as const;

let count = 0;

function genId() {
  count = (count + 1) % Number.MAX_SAFE_INTEGER;
  return count.toString();
}

type ActionType = typeof actionTypes;

type Action =
  | {
      type: ActionType["ADD_TOAST"];
      toast: ToasterToast;
    }
  | {
      type: ActionType["UPDATE_TOAST"];
      toast: Partial<ToasterToast>;
    }
  | {
      type: ActionType["DISMISS_TOAST"];
      toastId?: ToasterToast["id"];
    }
  | {
      type: ActionType["REMOVE_TOAST"];
      toastId?: ToasterToast["id"];
    };

interface State {
  toasts: ToasterToast[];
}

const toastTimeouts = new Map<string, ReturnType<typeof setTimeout>>();

const addToRemoveQueue = (toastId: string) => {
  if (toastTimeouts.has(toastId)) {
    return;
  }

  const timeout = setTimeout(() => {
    toastTimeouts.delete(toastId);
    dispatch({
      type: "REMOVE_TOAST",
      toastId: toastId,
    });
  }, TOAST_REMOVE_DELAY);

  toastTimeouts.set(toastId, timeout);
};

export const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case "ADD_TOAST":
      return {
        ...state,
        toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT),
      };

    case "UPDATE_TOAST":
      return {
        ...state,
        toasts: state.toasts.map((t) =>
          t.id === action.toast.id ? { ...t, ...action.toast } : t
        ),
      };

    case "DISMISS_TOAST": {
      const { toastId } = action;

      if (toastId) {
        addToRemoveQueue(toastId);
      } else {
        state.toasts.forEach((t) => {
          addToRemoveQueue(t.id);
        });
      }

      return {
        ...state,
        toasts: state.toasts.map((t) =>
          t.id === toastId || toastId === undefined
            ? {
                ...t,
                open: false,
              }
            : t
        ),
      };
    }
    case "REMOVE_TOAST":
      if (action.toastId === undefined) {
        return {
          ...state,
          toasts: [],
        };
      }
      return {
        ...state,
        toasts: state.toasts.filter((t) => t.id !== action.toastId),
      };
  }
};

const listeners: Array<(state: State) => void> = [];

let memoryState: State = { toasts: [] };

function dispatch(action: Action) {
  memoryState = reducer(memoryState, action);
  listeners.forEach((listener) => {
    listener(memoryState);
  });
}

type Toast = Omit<ToasterToast, "id">;

function toast({ ...props }: Toast) {
  const id = genId();

  const update = (updateProps: ToasterToast) =>
    dispatch({
      type: "UPDATE_TOAST",
      toast: { ...updateProps, id },
    });

  const dismiss = () => dispatch({ type: "DISMISS_TOAST", toastId: id });

  dispatch({
    type: "ADD_TOAST",
    toast: {
      ...props,
      id,
      open: true,
      onOpenChange: (open: boolean) => {
        if (!open) dismiss();
      },
    },
  });

  return {
    id: id,
    dismiss,
    update,
  };
}

function useToast() {
  const [state, setState] = React.useState<State>(memoryState);

  React.useEffect(() => {
    listeners.push(setState);
    return () => {
      const index = listeners.indexOf(setState);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    };
  }, [state]);

  return {
    ...state,
    toast,
    dismiss: (toastId?: string) => dispatch({ type: "DISMISS_TOAST", toastId }),
  };
}

export { useToast, toast };
''')
    files_created += 1

    # =====================================================================
    # SUMMARY
    # =====================================================================
    print("\n" + "=" * 60)
    print(f"✅ Phase 7 (FINAL) Complete!")
    print(f"   Total files created: {files_created}")
    print("=" * 60)
    print("\n📋 Files created:")
    print("   📄 app/[locale]/page.tsx          - Landing page")
    print("   📄 types/database.ts              - Database types (14 tables)")
    print("   📄 public/robots.txt              - SEO robots file")
    print("   📄 README.md                      - Complete documentation")
    print("   🎨 components/ui/button.tsx        - Button (6 variants, 4 sizes)")
    print("   🎨 components/ui/input.tsx         - Input field")
    print("   🎨 components/ui/textarea.tsx      - Textarea")
    print("   🎨 components/ui/label.tsx         - Label")
    print("   🎨 components/ui/badge.tsx         - Badge (6 variants)")
    print("   🎨 components/ui/card.tsx          - Card (6 sub-components)")
    print("   🎨 components/ui/skeleton.tsx      - Skeleton loader")
    print("   🎨 components/ui/separator.tsx     - Separator")
    print("   🎨 components/ui/avatar.tsx        - Avatar (3 sub-components)")
    print("   🎨 components/ui/dialog.tsx        - Dialog (8 sub-components)")
    print("   🎨 components/ui/dropdown-menu.tsx - Dropdown (14 sub-components)")
    print("   🎨 components/ui/select.tsx        - Select (10 sub-components)")
    print("   🎨 components/ui/tabs.tsx          - Tabs (3 sub-components)")
    print("   🎨 components/ui/tooltip.tsx       - Tooltip (4 sub-components)")
    print("   🎨 components/ui/switch.tsx        - Switch toggle")
    print("   🎨 components/ui/scroll-area.tsx   - Scroll area")
    print("   🎨 components/ui/table.tsx         - Table (8 sub-components)")
    print("   🎨 components/ui/toast.tsx         - Toast (8 sub-components)")
    print("   🎨 components/ui/toaster.tsx       - Toaster provider")
    print("   🪝 hooks/useToast.ts              - Toast hook")

    print("\n" + "=" * 60)
    print("🏁 ALL PHASES COMPLETE!")
    print("=" * 60)
    print("""
╔══════════════════════════════════════════════════════════╗
║                   FINAL CHECKLIST                        ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  ✅ All ~130 files created across all 7 phases           ║
║                                                          ║
║  📋 Setup Steps:                                         ║
║                                                          ║
║  1. Install dependencies:                                ║
║     $ npm install                                        ║
║                                                          ║
║  2. Install Radix UI peer dependencies:                  ║
║     $ npm install @radix-ui/react-slot                   ║
║       @radix-ui/react-dialog                             ║
║       @radix-ui/react-dropdown-menu                      ║
║       @radix-ui/react-select                             ║
║       @radix-ui/react-tabs                               ║
║       @radix-ui/react-tooltip                            ║
║       @radix-ui/react-switch                             ║
║       @radix-ui/react-scroll-area                        ║
║       @radix-ui/react-separator                          ║
║       @radix-ui/react-avatar                             ║
║       @radix-ui/react-toast                              ║
║       @radix-ui/react-label                              ║
║                                                          ║
║  3. Configure environment:                               ║
║     $ cp .env.example .env.local                         ║
║     # Edit .env.local with your Supabase & other keys    ║
║                                                          ║
║  4. Setup Supabase (run in SQL Editor in ORDER):         ║
║     ① supabase/schema.sql     (14 tables)                ║
║     ② supabase/rls-policies.sql (all RLS policies)       ║
║     ③ supabase/functions.sql  (7 functions + triggers)   ║
║     ④ supabase/seed.sql       (4 built-in personas)      ║
║                                                          ║
║  5. Set super admin email in Supabase:                   ║
║     ALTER DATABASE postgres                              ║
║       SET app.settings.super_admin_email =               ║
║       'your-admin@email.com';                            ║
║                                                          ║
║  6. Disable email confirmation in Supabase:              ║
║     Auth > Settings > Email > Confirm email: OFF         ║
║                                                          ║
║  7. Start development server:                            ║
║     $ npm run dev                                        ║
║                                                          ║
║  8. Register with SUPER_ADMIN_EMAIL to create admin      ║
║                                                          ║
║  9. Go to /admin to configure:                           ║
║     - Add global API keys for AI platforms               ║
║     - Add models for each API key                        ║
║     - Configure Telegram notifications                   ║
║                                                          ║
║  🌐 Deploy to Cloudflare:                                ║
║     $ npm run pages:build                                ║
║     $ npm run pages:deploy                               ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  📁 Project Structure Summary:                           ║
║     Phase 1A: Config + Database + Utils + Types           ║
║     Phase 1B: Supabase + Stores + i18n + Layout           ║
║     Phase 2:  Authentication (Login/Register/Guards)      ║
║     Phase 3:  Chat (Streaming/Messages/Sidebar)           ║
║     Phase 4:  API Keys + Encryption                       ║
║     Phase 5:  Personas + Settings + Export                ║
║     Phase 6:  Admin Dashboard + Notifications             ║
║     Phase 7:  Landing + UI Components + README (THIS)     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    main()

